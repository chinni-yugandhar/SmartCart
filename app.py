# app.py
from flask import Flask, render_template, request, redirect, session, flash, url_for,jsonify
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from flask import make_response,render_template
from utils.pdf_generator import generate_pdf
import mysql.connector
import bcrypt
import random
import config
import os
import razorpay

razorpay_client = razorpay.Client(
    auth=(config.RAZORPAY_KEY_ID, config.RAZORPAY_KEY_SECRET)
)


app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# ---------------- EMAIL CONFIGURATION ----------------
app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD

mail = Mail(app)


# ---------------- DB CONNECTION FUNCTION --------------
def get_db_connection():
    return mysql.connector.connect(
    host=config.DB_HOST,
    port=config.DB_PORT,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_NAME
)



# ---------------------------------------------------------
# ROUTE 0: HOMEPAGE LANDING
# ---------------------------------------------------------
@app.route('/')
def index():
    return render_template("index.html")


# ---------------------------------------------------------
# ROUTE 1: ADMIN SIGNUP (SEND OTP)
# ---------------------------------------------------------
@app.route('/admin-signup', methods=['GET', 'POST'])
def admin_signup():

    # Show form
    if request.method == "GET":
        return render_template("admin/admin_signup.html")

    # POST → Process signup
    name = request.form['name']
    email = request.form['email']

    # 1️ Check if admin email already exists
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT admin_id FROM admin WHERE email=%s", (email,))
    existing_admin = cursor.fetchone()
    cursor.close()
    conn.close()

    if existing_admin:
        flash("This email is already registered. Please login instead.", "danger")
        return redirect('/admin-signup')

    # 2️ Save user input temporarily in session
    session['signup_name'] = name
    session['signup_email'] = email

    # 3️ Generate OTP and store in session
    otp = random.randint(100000, 999999)
    session['otp'] = otp

    # 4️ Send OTP Email
    message = Message(
    subject="SmartCart Admin OTP",
    sender=config.MAIL_SENDER,
    recipients=[email]
)
    message.body = f"Your OTP for SmartCart Admin Registration is: {otp}"
    try:
        print("Before sending email")
        mail.send(message)
        print("Email sent successfully")
    except Exception as e:
        print("EMAIL ERROR:", repr(e))
        raise
    



# ---------------------------------------------------------
# ROUTE 2: DISPLAY OTP PAGE
# ---------------------------------------------------------
@app.route('/verify-otp', methods=['GET'])
def verify_otp_get():
    return render_template("admin/verify_otp.html")



# ---------------------------------------------------------
# ROUTE 3: VERIFY OTP + SAVE ADMIN
# ---------------------------------------------------------
@app.route('/verify-otp', methods=['POST'])
def verify_otp_post():
    
    # User submitted OTP + Password
    user_otp = request.form['otp']
    password = request.form['password']

    # Compare OTP
    if str(session.get('otp')) != str(user_otp):
        flash("Invalid OTP. Try again!", "danger")
        return redirect('/verify-otp')

    # Hash password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert admin into database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO admin (name, email, password) VALUES (%s, %s, %s)",
        (session['signup_name'], session['signup_email'], hashed_password)
    )
    conn.commit()
    cursor.close()
    conn.close()

    # Clear temporary session data
    session.pop('otp', None)
    session.pop('signup_name', None)
    session.pop('signup_email', None)

    flash("Admin Registered Successfully!", "success")
    return redirect('/admin-signup')

# =================================================================
# ROUTE 4: ADMIN LOGIN PAGE (GET + POST)
# =================================================================
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():

    # Show login page
    if request.method == 'GET':
        return render_template("admin/admin_login.html")

    # POST → Validate login
    email = request.form['email']
    password = request.form['password']

    # Step 1: Check if admin email exists
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM admin WHERE email=%s", (email,))
    admin = cursor.fetchone()

    cursor.close()
    conn.close()

    if admin is None:
        flash("Email not found! Please register first.", "danger")
        return redirect('/admin-login')

    # Step 2: Compare entered password with hashed password
    stored_hashed_password = admin['password'].encode('utf-8')

    if not bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
        flash("Incorrect password! Try again.", "danger")
        return redirect('/admin-login')

    # Step 5: If login success → Create admin session
    session['admin_id'] = admin['admin_id']
    session['admin_name'] = admin['name']
    session['admin_email'] = admin['email']

    flash("Login Successful!", "success")
    return redirect('/admin-dashboard')



# =================================================================
# ROUTE 5: ADMIN DASHBOARD (PROTECTED ROUTE)
# =================================================================
@app.route('/admin-dashboard')
def admin_dashboard():

    # Protect dashboard → Only logged-in admin can access
    if 'admin_id' not in session:
        flash("Please login to access dashboard!", "danger")
        return redirect('/admin-login')

    # Send admin name to dashboard UI
    return render_template("admin/dashboard.html", admin_name=session['admin_name'])



# =================================================================
# ROUTE 6: ADMIN LOGOUT
# =================================================================
@app.route('/admin-logout')
def admin_logout():

    # Clear admin session
    session.pop('admin_id', None)
    session.pop('admin_name', None)
    session.pop('admin_email', None)

    flash("Logged out successfully.", "success")
    return redirect('/admin-login')



# =================================================================
# ROUTE 7: SHOW ADD PRODUCT PAGE (Protected Route)
# =================================================================
@app.route('/admin/add-item', methods=['GET'])
def add_item_page():

    # Only logged-in admin can access
    if 'admin_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/admin-login')

    return render_template("admin/add_item.html")

import os
from werkzeug.utils import secure_filename

# ------------------- IMAGE UPLOAD PATH -------------------
PRODUCT_UPLOAD_FOLDER = 'static/uploads/product_images'
PROFILE_UPLOAD_FOLDER = 'static/uploads/profile_images'
ADMIN_UPLOAD_FOLDER = 'static/uploads/admin_profiles'

app.config['PRODUCT_UPLOAD_FOLDER'] = PRODUCT_UPLOAD_FOLDER
app.config['PROFILE_UPLOAD_FOLDER'] = PROFILE_UPLOAD_FOLDER
app.config['ADMIN_UPLOAD_FOLDER'] = ADMIN_UPLOAD_FOLDER



# =================================================================
# ROUTE 8: ADD PRODUCT INTO DATABASE
# =================================================================
@app.route('/admin/add-item', methods=['POST'])
def add_item():

    # Check admin session
    if 'admin_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/admin-login')

    # 1️ Get form data
    name = request.form['name']
    description = request.form['description']
    category = request.form['category']
    price = request.form['price']
    image_file = request.files['image']

    # 2️ Validate image upload
    if image_file.filename == "":
        flash("Please upload a product image!", "danger")
        return redirect('/admin/add-item')

    # 3️ Secure the file name
    filename = secure_filename(image_file.filename)

    # 4️ Create full path (product images)
    image_path = os.path.join(app.config['PRODUCT_UPLOAD_FOLDER'], filename)

    #  Save image into folder
    image_file.save(image_path)

    # 6️ Insert product into database
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (name, description, category, price, image) VALUES (%s, %s, %s, %s, %s)",
        (name, description, category, price, filename)
    )

    conn.commit()
    cursor.close()
    conn.close()

    flash("Product added successfully!", "success")
    return redirect('/admin/add-item')


# =================================================================
# ROUTE 9: UPDATED PRODUCT LIST WITH SEARCH + CATEGORY FILTER
# =================================================================
@app.route('/admin/item-list')
def item_list():

    if 'admin_id' not in session:
        flash("Please login!", "danger")
        return redirect('/admin-login')

    search = request.args.get('search', '')
    category_filter = request.args.get('category', '')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1️⃣ Fetch category list for dropdown
    cursor.execute("SELECT DISTINCT category FROM products")
    categories = cursor.fetchall()

    # 2️⃣ Build dynamic query based on filters
    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if search:
        query += " AND name LIKE %s"
        params.append("%" + search + "%")

    if category_filter:
        query += " AND category = %s"
        params.append(category_filter)

    cursor.execute(query, params)
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admin/item_list.html",
        products=products,
        categories=categories
    )


#==================================================================
# ROUTE 10: VIEW SINGLE PRODUCT DETAILS
# =================================================================
@app.route('/admin/view-item/<int:item_id>')
def view_item(item_id):

    # Check admin session
    if 'admin_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/admin-login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products WHERE product_id = %s", (item_id,))
    product = cursor.fetchone()

    cursor.close()
    conn.close()

    if not product:
        flash("Product not found!", "danger")
        return redirect('/admin/item-list')

    return render_template("admin/view_item.html", product=product)

# =================================================================
# ROUTE 11: SHOW UPDATE FORM WITH EXISTING DATA
# =================================================================
@app.route('/admin/update-item/<int:item_id>', methods=['GET'])
def update_item_page(item_id):

    # Check login
    if 'admin_id' not in session:
        flash("Please login!", "danger")
        return redirect('/admin-login')

    # Fetch product data
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products WHERE product_id = %s", (item_id,))
    product = cursor.fetchone()

    cursor.close()
    conn.close()

    if not product:
        flash("Product not found!", "danger")
        return redirect('/admin/item-list')

    return render_template("admin/update_item.html", product=product)


# =================================================================
# ROUTE-12: UPDATE PRODUCT + OPTIONAL IMAGE REPLACE
# =================================================================
@app.route('/admin/update-item/<int:item_id>', methods=['POST'])
def update_item(item_id):

    if 'admin_id' not in session:
        flash("Please login!", "danger")
        return redirect('/admin-login')

    # 1️ Get updated form data
    name = request.form['name']
    description = request.form['description']
    category = request.form['category']
    price = request.form['price']

    new_image = request.files.get('image')

    # 2️ Fetch old product data
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE product_id = %s", (item_id,))
    product = cursor.fetchone()

    if not product:
        flash("Product not found!", "danger")
        return redirect('/admin/item-list')

    old_image_name = product['image']

    # 3️ If admin uploaded a new image → replace it
    if new_image and new_image.filename != "":
        
        # Secure 
        
        
        from werkzeug.utils import secure_filename
        new_filename = secure_filename(new_image.filename)

        # Save new image (product images)
        new_image_path = os.path.join(app.config['PRODUCT_UPLOAD_FOLDER'], new_filename)
        new_image.save(new_image_path)

        # Delete old image file (product images)
        old_image_path = os.path.join(app.config['PRODUCT_UPLOAD_FOLDER'], old_image_name)
        if os.path.exists(old_image_path):
            os.remove(old_image_path)

        final_image_name = new_filename

    else:
        # No new image uploaded → keep old one
        final_image_name = old_image_name

    # 4️ Update product in the database
    cursor.execute("""
        UPDATE products
        SET name=%s, description=%s, category=%s, price=%s, image=%s
        WHERE product_id=%s
    """, (name, description, category, price, final_image_name, item_id))

    conn.commit()

    # Fetch the updated product so the form shows the latest values
    cursor.execute("SELECT * FROM products WHERE product_id = %s", (item_id,))
    updated_product = cursor.fetchone()

    cursor.close()
    conn.close()

    flash("Product updated successfully!", "success")
    return render_template("admin/update_item.html", product=updated_product)


# =================================================================
#  route-13 DELETE PRODUCT (DELETE DB ROW + DELETE IMAGE FILE)
# =================================================================
@app.route('/admin/delete-item/<int:item_id>')
def delete_item(item_id):

    if 'admin_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/admin-login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1️ Fetch product to get image name
    cursor.execute("SELECT image FROM products WHERE product_id=%s", (item_id,))
    product = cursor.fetchone()

    if not product:
        flash("Product not found!", "danger")
        return redirect('/admin/item-list')

    image_name = product['image']

    # Delete image from product folder
    image_path = os.path.join(app.config['PRODUCT_UPLOAD_FOLDER'], image_name)
    if os.path.exists(image_path):
        os.remove(image_path)

    # 2️ Delete product from DB
    cursor.execute("DELETE FROM products WHERE product_id=%s", (item_id,))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Product deleted successfully!", "success")
    return redirect('/admin/item-list')


ADMIN_UPLOAD_FOLDER = 'static/uploads/admin_profiles'
app.config['ADMIN_UPLOAD_FOLDER'] = ADMIN_UPLOAD_FOLDER


# =================================================================
# ROUTE 14: SHOW ADMIN PROFILE DATA
# =================================================================
@app.route('/admin/profile', methods=['GET'])
def admin_profile():

    if 'admin_id' not in session:
        flash("Please login!", "danger")
        return redirect('/admin-login')

    admin_id = session['admin_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM admin WHERE admin_id = %s", (admin_id,))
    admin = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("admin/admin_profile.html", admin=admin)

# This route updates name + email + password (optional) + image (optional).
# =================================================================
# ROUTE 15: UPDATE ADMIN PROFILE (NAME, EMAIL, PASSWORD, IMAGE)
# =================================================================
@app.route('/admin/profile', methods=['POST'])
def admin_profile_update():

    if 'admin_id' not in session:
        flash("Please login!", "danger")
        return redirect('/admin-login')

    admin_id = session['admin_id']

    # 1️ Get form data
    name = request.form['name']
    email = request.form['email']
    new_password = request.form['password']
    new_image = request.files['profile_image']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 2️ Fetch old admin data
    cursor.execute("SELECT * FROM admin WHERE admin_id = %s", (admin_id,))
    admin = cursor.fetchone()

    old_image_name = admin['profile_image']

    # 3️ Update password only if entered
    if new_password:
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    else:
        hashed_password = admin['password']  # keep old password

    # 4️ Process new profile image if uploaded
    if new_image and new_image.filename != "":
        
        from werkzeug.utils import secure_filename
        new_filename = secure_filename(new_image.filename)

        # Save new image
        image_path = os.path.join(app.config['ADMIN_UPLOAD_FOLDER'], new_filename)
        new_image.save(image_path)

        # Delete old image
        if old_image_name:
            old_image_path = os.path.join(app.config['ADMIN_UPLOAD_FOLDER'], old_image_name)
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

        final_image_name = new_filename
    else:
        final_image_name = old_image_name

    # 5️ Update database
    cursor.execute("""
        UPDATE admin
        SET name=%s, email=%s, password=%s, profile_image=%s
        WHERE admin_id=%s
    """, (name, email, hashed_password, final_image_name, admin_id))

    conn.commit()
    cursor.close()
    conn.close()

    # Update session name for UI consistency
    session['admin_name'] = name  
    session['admin_email'] = email

    flash("Profile updated successfully!", "success")
    return redirect('/admin/profile')


#.................... USER MODULE START....................

# ---------------------------------------------------------
# ROUTE 16: USER SIGNUP (SEND OTP)
# ---------------------------------------------------------
@app.route('/user-signup', methods=['GET', 'POST'])
def user_signup():

    # Show form
    if request.method == "GET":
        return render_template("user/user_signup.html")

    # POST → Process signup
    name = request.form['name']
    email = request.form['email']

    # 1️ Check if user email already exists
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id FROM users WHERE email=%s", (email,))
    existing_user = cursor.fetchone()
    cursor.close()
    conn.close()

    if existing_user:
        flash("This email is already registered. Please login instead.", "danger")
        return redirect('/user-login')

    # 2️ Save user input temporarily in session
    session['user_signup_name'] = name
    session['user_signup_email'] = email

    # 3️ Generate OTP and store in session
    otp = random.randint(100000, 999999)
    session['user_otp'] = otp

    # 4️ Send OTP Email
    message = Message(
        subject="SmartCart User OTP",
        sender=config.MAIL_USERNAME,
        recipients=[email]
    )
    message.body = f"Your OTP for SmartCart User Registration is: {otp}"
    mail.send(message)

    flash("OTP sent to your email!", "success")
    return redirect('/user-verify-otp')

# ---------------------------------------------------------
# ROUTE 17: DISPLAY USER OTP PAGE
# ---------------------------------------------------------
@app.route('/user-verify-otp', methods=['GET'])
def user_verify_otp_get():
    return render_template("user/verify_otp.html")

# ---------------------------------------------------------
# ROUTE 18: VERIFY USER OTP + SAVE USER
# ---------------------------------------------------------
@app.route('/user-verify-otp', methods=['POST'])
def user_verify_otp_post():

    # User submitted OTP + Password
    user_otp = request.form['otp']
    password = request.form['password']

    # Compare OTP
    if str(session.get('user_otp')) != str(user_otp):
        flash("Invalid OTP. Try again!", "danger")
        return redirect('/user-verify-otp')

    # Hash password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert user into database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (session['user_signup_name'], session['user_signup_email'], hashed_password)
    )
    conn.commit()
    cursor.close()
    conn.close()

    # Clear temporary session data
    session.pop('user_otp', None)
    session.pop('user_signup_name', None)
    session.pop('user_signup_email', None)

    flash("User Registered Successfully!", "success")
    return redirect('/user-signup')

# =================================================================
# ROUTE 19: USER LOGIN PAGE (GET + POST)
# =================================================================
@app.route('/user-login', methods=['GET', 'POST'])
def user_login():

    # Show login page
    if request.method == 'GET':
        return render_template("user/user_login.html")

    # POST → Validate login
    email = request.form['email']
    password = request.form['password']

    # Step 1: Check if user email exists
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user is None:
        flash("Email not found! Please register first.", "danger")
        return redirect('/user-login')

    # Step 2: Compare entered password with hashed password
    stored_hashed_password = user['password'].encode('utf-8') if isinstance(user['password'], str) else user['password']

    if not bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
        flash("Incorrect password! Try again.", "danger")
        return redirect('/user-login')

    # Step 3: If login success → Create user session
    session['user_id'] = user['user_id']
    session['user_name'] = user['name']
    session['user_email'] = user['email']

    flash("Login Successful!", "success")
    return redirect('/user-dashboard')

# =========================================================
#  ROUTE 20: USER FORGOT PASSWORD - SEND OTP
# =========================================================
@app.route('/user-forgot-password', methods=['GET', 'POST'])
def user_forgot_password():

    if request.method == 'GET':
        return render_template('user/forgot_password.html')

    email = request.form['email']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user is None:
        flash("Email not found!", "danger")
        return redirect('/user-forgot-password')

    otp = random.randint(100000, 999999)
    session['reset_email'] = email
    session['reset_otp'] = otp

    message = Message(
        subject="SmartCart Password Reset OTP",
        sender=config.MAIL_USERNAME,
        recipients=[email]
    )
    message.body = f"Your OTP for password reset is: {otp}"
    mail.send(message)

    flash("OTP sent to your email!", "success")
    return redirect('/user-reset-password')

# =========================================================
#  ROUTE 21: USER RESET PASSWORD (OTP VERIFY + NEW PASSWORD)
# =========================================================
@app.route('/user-reset-password', methods=['GET', 'POST'])
def user_reset_password():

    if request.method == 'GET':
        return render_template('user/reset_password.html')

    entered_otp = request.form['otp']
    new_password = request.form['password']
    confirm_password = request.form['confirm_password']

    if str(session.get('reset_otp')) != str(entered_otp):
        flash("Invalid OTP!", "danger")
        return redirect('/user-reset-password')

    if new_password != confirm_password:
        flash("Passwords do not match!", "danger")
        return redirect('/user-reset-password')

    hashed_password = bcrypt.hashpw(
        new_password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET password=%s WHERE email=%s",
        (hashed_password, session['reset_email'])
    )
    conn.commit()
    cursor.close()
    conn.close()

    session.pop('reset_email', None)
    session.pop('reset_otp', None)

    flash("Password reset successful! Please login.", "success")
    return redirect('/user-login')


# 

# =================================================================
# ROUTE 22: USER DASHBOARD (PROTECTED ROUTE)
# =================================================================
@app.route('/user-dashboard')
def user_dashboard():

    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/user-login')

    cart = session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())

    return render_template(
        "user/dashboard.html",
        user_name=session['user_name'],
        cart_count=cart_count
    )


# =================================================================
# ROUTE 23: USER LOGOUT
# =================================================================
@app.route('/user-logout')
def user_logout():

    # Clear user session
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_email', None)

    flash("Logged out successfully.", "success")
    return redirect('/user-login')

# =================================================================
#   ROUTE 24: USER PRODUCT LISTING (SEARCH + FILTER)
# =================================================================
@app.route('/user/products')
def user_products():

    if 'user_id' not in session:
        flash("Please login to view products!", "danger")
        return redirect('/user-login')

    search = request.args.get('search', '')
    category_filter = request.args.get('category', '')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch categories
    cursor.execute("SELECT DISTINCT category FROM products")
    categories = cursor.fetchall()

    # Build query
    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if search:
        query += " AND name LIKE %s"
        params.append("%" + search + "%")

    if category_filter:
        query += " AND category = %s"
        params.append(category_filter)

    cursor.execute(query, params)
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "user/user_products.html",
        products=products,
        categories=categories
    )


# =================================================================
#   ROUTE 25: USER PRODUCT DETAILS
# =================================================================
@app.route('/user/product/<int:product_id>')
def user_product_details(product_id):

    if 'user_id' not in session:
        flash("Please login!", "danger")
        return redirect('/user-login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()

    cursor.close()
    conn.close()

    if not product:
        flash("Product not found!", "danger")
        return redirect('/user/products')

    return render_template("user/product_details.html", product=product)


# PROFILE_UPLOAD_FOLDER already configured above; do not override


# =================================================================
#  ROUTE 26: USER PROFILE VIEW
# =================================================================
@app.route('/user/profile')
def user_profile():

    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/user-login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE user_id=%s", (session['user_id'],))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("user/profile.html", user=user)


# =================================================================
#  ROUTE 27: USER PROFILE EDIT
# =================================================================
@app.route('/user/profile/edit', methods=['GET', 'POST'])
def edit_user_profile():

    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/user-login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'GET':
        cursor.execute("SELECT * FROM users WHERE user_id=%s", (session['user_id'],))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template("user/edit_profile.html", user=user)

    name = request.form['name']
    phone = request.form['phone']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    pincode = request.form['pincode']

    cursor.execute("SELECT profile_image FROM users WHERE user_id=%s", (session['user_id'],))
    existing_user = cursor.fetchone()
    profile_image = existing_user['profile_image']

    if 'profile_image' in request.files:
        file = request.files['profile_image']
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile_image = filename

    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET name=%s, phone=%s, address=%s, city=%s, state=%s, pincode=%s, profile_image=%s
        WHERE user_id=%s
    """, (name, phone, address, city, state, pincode, profile_image, session['user_id']))
    conn.commit()
    cursor.close()
    conn.close()

    session['user_name'] = name

    flash("Profile updated successfully!", "success")
    return redirect('/user/profile')

# =================================================================
#                    USER CART SYSTEM
# =================================================================

# ---------------------------------------------------------
#  Route 28 :HELPER - CART ITEM COUNT
# ---------------------------------------------------------
def get_cart_count():
    cart = session.get('cart', {})
    return sum(item['quantity'] for item in cart.values())

# ---------------------------------------------------------
# ROUTE 29: ADD TO CART (NORMAL)
# ---------------------------------------------------------
@app.route('/user/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):

    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/user-login')

    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE product_id=%s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()

    if not product:
        flash("Product not found.", "danger")
        return redirect('/user/products')

    pid = str(product_id)

    if pid in cart:
        cart[pid]['quantity'] += 1
    else:
        cart[pid] = {
            'name': product['name'],
            'price': float(product['price']),
            'image': product['image'],
            'quantity': 1
        }

    session['cart'] = cart
    session.modified = True

    flash("Item added to cart!", "success")
    return redirect('/user/products')


# ---------------------------------------------------------
# ROUTE 30: QUICK ADD TO CART
# ---------------------------------------------------------
@app.route('/user/cart/quick-add/<int:product_id>', methods=['POST'])
def quick_add_to_cart(product_id):

    if 'user_id' not in session:
        return jsonify({
            "status": "error",
            "message": "Please login first!"
        }), 401

    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE product_id=%s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()

    if not product:
        return jsonify({
            "status": "error",
            "message": "Product not found!"
        }), 404

    pid = str(product_id)

    if pid in cart:
        cart[pid]['quantity'] += 1
    else:
        cart[pid] = {
            'name': product['name'],
            'price': float(product['price']),
            'image': product['image'],
            'quantity': 1
        }

    session['cart'] = cart
    session.modified = True

    return jsonify({
        "status": "success",
        "message": "Item added to cart!",
        "cart_count": get_cart_count()
    })

# ---------------------------------------------------------
# ROUTE 31: VIEW CART
# ---------------------------------------------------------
@app.route('/user/cart')
def view_cart():

    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/user-login')

    cart = session.get('cart', {})
    grand_total = sum(item['price'] * item['quantity'] for item in cart.values())

    return render_template(
        "user/cart.html",
        cart=cart,
        grand_total=grand_total
    )


# ---------------------------------------------------------
# ROUTE 32: INCREASE QUANTITY
# ---------------------------------------------------------
@app.route('/user/cart/increase/<pid>', methods=['POST'])
def increase_quantity(pid):

    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/user-login')

    cart = session.get('cart', {})

    if pid in cart:
        cart[pid]['quantity'] += 1

    session['cart'] = cart
    session.modified = True

    return redirect('/user/cart')


# ---------------------------------------------------------
# ROUTE 33: DECREASE QUANTITY
# ---------------------------------------------------------
@app.route('/user/cart/decrease/<pid>', methods=['POST'])
def decrease_quantity(pid):

    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/user-login')

    cart = session.get('cart', {})

    if pid in cart:
        cart[pid]['quantity'] -= 1

        if cart[pid]['quantity'] <= 0:
            cart.pop(pid)

    session['cart'] = cart
    session.modified = True

    return redirect('/user/cart')


# ---------------------------------------------------------
# ROUTE 34: REMOVE ITEM
# ---------------------------------------------------------
@app.route('/user/cart/remove/<pid>', methods=['POST'])
def remove_from_cart(pid):

    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/user-login')

    cart = session.get('cart', {})

    if pid in cart:
        cart.pop(pid)

    session['cart'] = cart
    session.modified = True

    flash("Item removed from cart!", "success")
    return redirect('/user/cart')

# =================================================================
# ROUTE 35: CHECKOUT SELECTED CART ITEMS
# =================================================================
@app.route('/user/cart/checkout', methods=['POST'])
def checkout_cart():

    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/user-login')

    cart = session.get('cart', {})
    selected_ids = request.form.getlist('selected_items')

    if not selected_ids:
        flash("Please select at least one item to buy.", "danger")
        return redirect('/user/cart')

    selected_items = []
    for pid in selected_ids:
        item = cart.get(pid)
        if item:
            selected_items.append({
                'product_id': pid,
                'name': item['name'],
                'price': item['price'],
                'image': item['image'],
                'quantity': item['quantity'],
                'total': item['price'] * item['quantity']
            })

    if not selected_items:
        flash("Selected items are not available in the cart.", "danger")
        return redirect('/user/cart')

    session['cart_checkout'] = {
        'items': selected_items,
        'total_amount': sum(item['total'] for item in selected_items)
    }
    session.modified = True

    return redirect('/user/cart/address')


# =================================================================
# ROUTE 36: PROCEED TO BUY SELECTED CART ITEMS
# =================================================================
@app.route('/user/cart/proceed-buy', methods=['POST'])
def cart_proceed_buy():

    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/user-login')

    cart = session.get('cart', {})
    selected_items = request.form.getlist('selected_items')

    # If the user didn't explicitly select items, proceed with the whole cart.
    if not selected_items:
        selected_items = list(cart.keys())

    if not selected_items:
        flash("Your cart is empty. Please add items before proceeding.", "danger")
        return redirect('/user/cart')

    selected_cart_items = []
    total_amount = 0

    for pid in selected_items:
        if pid in cart:
            item = cart[pid]
            selected_cart_items.append({
                'product_id': pid,
                'name': item['name'],
                'price': item['price'],
                'image': item['image'],
                'quantity': item['quantity'],
                'total': item['price'] * item['quantity']
            })
            total_amount += item['price'] * item['quantity']

    if not selected_cart_items:
        flash("Selected items were not found in the cart.", "danger")
        return redirect('/user/cart')

    session['cart_checkout'] = {
        'items': selected_cart_items,
        'total_amount': total_amount
    }
    session['checkout_source'] = 'cart'
    session.modified = True

    return redirect('/user/cart/address')

# =================================================================
# ROUTE 37: CART ADDRESS PAGE (GET + POST)
# =================================================================
@app.route('/user/cart/address', methods=['GET', 'POST'])
def address():

    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/user-login')

    checkout = session.get('cart_checkout')
    if not checkout:
        flash("No cart checkout data found.", "danger")
        return redirect('/user/cart')

    if request.method == 'GET':
        return render_template('user/address.html', checkout=checkout)

    full_name = request.form['full_name']
    mobile = request.form['mobile']
    email = request.form['email']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    pincode = request.form['pincode']

    session['checkout_data'] = {
        'items': checkout['items'],
        'total_amount': checkout['total_amount'],
        'full_name': full_name,
        'mobile': mobile,
        'email': email,
        'address': address,
        'city': city,
        'state': state,
        'pincode': pincode
    }
    session.pop('cart_checkout', None)
    session.modified = True

    flash("Address saved successfully!", "success")
    return redirect('/payment')

# =================================================================
# ROUTE 38: BUY NOW → ADDRESS CHECKOUT PAGE
# =================================================================
@app.route('/buy-now/<int:product_id>', methods=['GET'])
def buy_now(product_id):

    # Check user login
    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/user-login')

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get selected product details
    cursor.execute("SELECT * FROM products WHERE product_id=%s", (product_id,))
    product = cursor.fetchone()

    # If product not found
    if not product:
        cursor.close()
        conn.close()
        flash("Product not found!", "danger")
        return redirect('/user-dashboard')

    # Prepare a single-item checkout payload and redirect to the common address page
    checkout = {
        'items': [{
            'product_id': str(product['product_id']),
            'name': product['name'],
            'price': float(product['price']),
            'image': product['image'],
            'quantity': 1,
            'total': float(product['price'])
        }],
        'total_amount': float(product['price'])
    }

    session['cart_checkout'] = checkout
    session['checkout_source'] = 'buy_now'
    session.modified = True

    cursor.close()
    conn.close()

    return redirect('/user/cart/address')


# =================================================================
# ROUTE 39: PAYMENT PAGE
# =================================================================
@app.route('/payment')
def payment():

    # Check user login
    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/user-login')

    # Get checkout data from session
    checkout_data = session.get('checkout_data')

    # If checkout data not found
    if not checkout_data:
        flash("No checkout data found!", "danger")
        return redirect('/user-dashboard')

    if 'total_amount' in checkout_data:
        total_amount = checkout_data['total_amount']
    else:
        total_amount = float(checkout_data.get('product_price', 0)) * int(checkout_data.get('quantity', 1))

    razorpay_amount = int(total_amount * 100)
    try:
        razorpay_order = razorpay_client.order.create({
            "amount": razorpay_amount,
            "currency": "INR",
            "payment_capture": 1
        })
    except Exception as e:
        app.logger.exception("Razorpay order creation failed")
        flash("Payment setup failed. Please try again later.", "danger")
        return redirect('/user/cart')

    session['razorpay_order_id'] = razorpay_order['id']
    session.modified = True

    return render_template(
        'user/payment.html',
        amount=total_amount,
        key_id=config.RAZORPAY_KEY_ID,
        order_id=razorpay_order['id'],
        customer_name=checkout_data.get('full_name', ''),
        customer_email=checkout_data.get('email', ''),
        customer_contact=checkout_data.get('mobile', '')
    )

# =================================================================
# ROUTE 40: PLACE ORDER / CONFIRM PAYMENT
# =================================================================
@app.route('/place-order', methods=['POST'])
def place_order():

    # Check user login
    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/user-login')

    # Get checkout data from session
    checkout_data = session.get('checkout_data')

    # If checkout data missing
    if not checkout_data:
        flash("Session expired. Please try again.", "danger")
        return redirect('/user-dashboard')

    # Example: Here you can save order into database later
    # For now, just clear checkout session after order placed
    session.pop('checkout_data', None)

    flash("Order placed successfully!", "success")
    return redirect('/user-dashboard')

# =================================================================
# ROUTE 41 : CREATE RAZORPAY ORDER
# =================================================================
@app.route('/user/pay')
def user_pay():

    if 'user_id' not in session:
        flash("Please login!", "danger")
        return redirect('/user-login')

    cart = session.get('cart', {})

    if not cart:
        flash("Your cart is empty!", "danger")
        return redirect('/user/products')

    # Calculate total amount
    total_amount = sum(item['price'] * item['quantity'] for item in cart.values())
    razorpay_amount = int(total_amount * 100)  # convert to paise

    # Create Razorpay order
    try:
        razorpay_order = razorpay_client.order.create({
            "amount": razorpay_amount,
            "currency": "INR",
            "payment_capture": 1
        })
    except Exception:
        app.logger.exception("Razorpay order creation failed for cart checkout")
        flash("Payment setup failed. Please try again later.", "danger")
        return redirect('/user/cart')

    session['razorpay_order_id'] = razorpay_order['id']

    return render_template(
        "user/payment.html",
        amount=total_amount,
        key_id=config.RAZORPAY_KEY_ID,
        order_id=razorpay_order['id']
    )



# ------------------------------
# ROUTE 42: Verify Payment and Store Order
# ------------------------------
@app.route('/verify-payment', methods=['POST'])
def verify_payment():
    if 'user_id' not in session:
        flash("Please login to complete the payment.", "danger")
        return redirect('/user-login')

    # Read values posted from frontend
    razorpay_payment_id = request.form.get('razorpay_payment_id')
    razorpay_order_id = request.form.get('razorpay_order_id')
    razorpay_signature = request.form.get('razorpay_signature')

    if not (razorpay_payment_id and razorpay_order_id and razorpay_signature):
        flash("Payment verification failed (missing data).", "danger")
        return redirect('/user/cart')

    # Build verification payload required by Razorpay client.utility
    payload = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
    }

    try:
        # This will raise an error if signature invalid
        razorpay_client.utility.verify_payment_signature(payload)

    except Exception as e:
        # Verification failed
        app.logger.error("Razorpay signature verification failed: %s", str(e))
        flash("Payment verification failed. Please contact support.", "danger")
        return redirect('/user/cart')

    # Signature verified — now store order and items into DB
    user_id = session['user_id']
    cart = session.get('cart', {})
    checkout_data = session.get('checkout_data')

    if not cart and not checkout_data:
        flash("No checkout data found. Cannot complete order.", "danger")
        return redirect('/user/cart')

    if checkout_data:
        items_to_store = checkout_data.get('items', [])
        total_amount = checkout_data.get('total_amount', 0)
    else:
        items_to_store = []
        for pid_str, item in cart.items():
            items_to_store.append({
                'product_id': int(pid_str),
                'name': item['name'],
                'quantity': item['quantity'],
                'price': item['price']
            })
        total_amount = sum(item['price'] * item['quantity'] for item in cart.values())

    # DB insert: orders and order_items
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Insert into orders table
        cursor.execute("""
            INSERT INTO orders (user_id, razorpay_order_id, razorpay_payment_id, amount, payment_status)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, razorpay_order_id, razorpay_payment_id, total_amount, 'paid'))

        order_db_id = cursor.lastrowid  # newly created order's primary key

        # Insert all items
        for item in items_to_store:
            product_id = int(item.get('product_id'))
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, product_name, quantity, price)
                VALUES (%s, %s, %s, %s, %s)
            """, (order_db_id, product_id, item.get('name'), item.get('quantity'), item.get('price')))

        # Commit transaction
        conn.commit()

        # Preserve delivery address for order success page
        if checkout_data:
            session['recent_order_address'] = {
                'full_name': checkout_data.get('full_name'),
                'mobile': checkout_data.get('mobile'),
                'email': checkout_data.get('email'),
                'address': checkout_data.get('address'),
                'city': checkout_data.get('city'),
                'state': checkout_data.get('state'),
                'pincode': checkout_data.get('pincode')
            }

        # Clear session data used for the checkout flow
        checkout_source = session.get('checkout_source')
        if checkout_source == 'cart':
            session.pop('cart', None)
        session.pop('checkout_data', None)
        session.pop('cart_checkout', None)
        session.pop('checkout_source', None)
        session.pop('razorpay_order_id', None)

        flash("Payment successful and order placed!", "success")
        return redirect(f"/user/order-success/{order_db_id}")

    except Exception as e:
        # Rollback and log error
        conn.rollback()
        app.logger.error("Order storage failed: %s\n%s", str(e), traceback.format_exc())
        flash("There was an error saving your order. Contact support.", "danger")
        return redirect('/user/cart')

    finally:
        cursor.close()
        conn.close()

        #  Route: Order Success Page
# Create a page to show order confirmation and order id:
@app.route('/user/order-success/<int:order_db_id>')
def order_success(order_db_id):
    if 'user_id' not in session:
        flash("Please login!", "danger")
        return redirect('/user-login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM orders WHERE order_id=%s AND user_id=%s", (order_db_id, session['user_id']))
    order = cursor.fetchone()

    cursor.execute("SELECT * FROM order_items WHERE order_id=%s", (order_db_id,))
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    if not order:
        flash("Order not found.", "danger")
        return redirect('/user/products')

    order_address = session.pop('recent_order_address', None)

    return render_template('user/oder_success.html', order=order, items=items, order_address=order_address)


# =================================================================
# ROUTE 43: PAYMENT SUCCESS PAGE 
# =================================================================
@app.route('/payment-success')
def payment_success():

    payment_id = request.args.get('payment_id')
    order_id = request.args.get('order_id')

    if not payment_id:
        flash("Payment failed!", "danger")
        return redirect('/user/cart')

    return render_template(
        "user/payment_success.html",
        payment_id=payment_id,
        order_id=order_id
        
    )

from flask import request, jsonify, render_template
import razorpay
import traceback

# Ensure razorpay_client is initialized (from Day 12)
# razorpay_client = razorpay.Client(auth=(config.RAZORPAY_KEY_ID, config.RAZORPAY_KEY_SECRET))

# ----------------------------
# ROUTE 44 :GENERATE INVOICE PDF
# ----------------------------
@app.route("/user/download-invoice/<int:order_id>")
def download_invoice(order_id):

    if 'user_id' not in session:
        flash("Please login!", "danger")
        return redirect('/user-login')

    # Fetch order
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM orders WHERE order_id=%s AND user_id=%s",
                   (order_id, session['user_id']))
    order = cursor.fetchone()

    cursor.execute("SELECT * FROM order_items WHERE order_id=%s", (order_id,))
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    if not order:
        flash("Order not found.", "danger")
        return redirect('/user/my-orders')

    # Render invoice HTML with customer and address details
    html = render_template(
        "user/invoice.html",
        order=order,
        items=items,
        customer_name=order.get('full_name', ''),
        customer_email=order.get('email', ''),
        customer_phone=order.get('mobile', ''),
        address=order.get('address', ''),
        city=order.get('city', ''),
        state=order.get('state', ''),
        pincode=order.get('pincode', '')
    )

    pdf = generate_pdf(html)
    if not pdf:
        flash("Error generating PDF", "danger")
        return redirect('/user/my-orders')

    # Prepare response
    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f"attachment; filename=invoice_{order_id}.pdf"

    return response


@app.route('/user/my-orders')
def user_my_orders():
    if 'user_id' not in session:
        flash("Please login!", "danger")
        return redirect('/user-login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM orders WHERE user_id=%s ORDER BY order_id DESC",
        (session['user_id'],)
    )
    orders = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('user/my_orders.html', orders=orders)






if __name__ == '__main__':
    app.run(debug=True)