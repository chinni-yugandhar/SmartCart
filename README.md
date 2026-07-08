# 🛒 SmartCart – Flask E-Commerce Web Application

SmartCart is a full-stack E-Commerce web application developed using **Python Flask**, **MySQL**, **HTML**, **CSS**, **Bootstrap**, **JavaScript**, **Razorpay Payment Gateway**, and **SMTP Email Services**.

The application provides a complete online shopping experience where customers can register, browse products, add items to their cart, make secure payments, download invoices, and manage their orders. It also includes an administrator panel for managing products and monitoring the store.

---

# 📌 Project Overview

SmartCart is designed to simulate a real-world online shopping platform. It includes secure authentication, OTP verification, product management, shopping cart functionality, online payment integration using Razorpay, invoice generation, and an admin dashboard.

---

# 🚀 Technologies Used

### Backend

* Python
* Flask
* MySQL
* Flask-Mail
* Razorpay API
* xhtml2pdf

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript
* Jinja2 Templates

### Database

* MySQL

### Tools

* Visual Studio Code
* Git
* GitHub

---

# 📁 Project Folder Structure

```text
Smart-cart-version-1-main/
│
├── app.py
├── config.py
├── README.md
│
├── static/
│   ├── css/
│   │   └── styles.css
│   │
│   └── uploads/
│       ├── admin_profiles/
│       ├── profile_images/
│       └── product_images/
│
├── templates/
│   │
│   ├── base.html
│   ├── index.html
│   │
│   ├── admin/
│   │   ├── admin_login.html
│   │   ├── admin_signup.html
│   │   ├── verify_otp.html
│   │   ├── dashboard.html
│   │   ├── admin_profile.html
│   │   ├── add_item.html
│   │   ├── update_item.html
│   │   ├── item_list.html
│   │   └── view_item.html
│   │
│   └── user/
│       ├── user_signup.html
│       ├── verify_otp.html
│       ├── user_login.html
│       ├── forgot_password.html
│       ├── reset_password.html
│       ├── dashboard.html
│       ├── profile.html
│       ├── edit_profile.html
│       ├── user_products.html
│       ├── product_details.html
│       ├── cart.html
│       ├── address.html
│       ├── payment.html
│       ├── payment_success.html
│       ├── invoice.html
│       ├── my_orders.html
│       ├── oder_success.html
│       └── buy_now.html
│
└── utils/
    └── pdf_generator.py
```

---

# 👨‍💼 Admin Module

The administrator has complete control over the application.

## Authentication

* Admin Registration
* OTP Verification
* Admin Login
* Secure Logout

## Dashboard

* Admin Dashboard
* Profile Management
* Product Statistics

## Product Management (CRUD)

### Create

* Add New Product
* Upload Product Image

### Read

* View Product List
* Search Products
* View Product Details

### Update

* Edit Product Information
* Replace Product Images

### Delete

* Remove Products

---

# 👤 User Module

## Authentication

* User Registration
* OTP Verification
* Secure Login
* Forgot Password
* Password Reset
* Logout

## Profile Management

* View Profile
* Edit Profile
* Upload Profile Picture

---

# 🛍 Product Module

Users can

* Browse Products
* Search Products
* View Product Details
* Filter Products
* View Product Images

---

# 🛒 Shopping Cart Operations

Users can

* Add Product to Cart
* View Cart
* Update Quantity
* Remove Product
* Calculate Total Amount
* Proceed to Checkout

---

# 📍 Address Module

* Add Delivery Address
* Update Shipping Details
* Store Delivery Information

---

# 💳 Razorpay Payment Integration

SmartCart integrates Razorpay for secure online payments.

### Payment Flow

Product Selection

↓

Shopping Cart

↓

Address Confirmation

↓

Checkout

↓

Razorpay Payment Gateway

↓

Payment Verification

↓

Order Confirmation

↓

Invoice Generation

↓

Order Stored Successfully

---

# 🧾 Invoice Generation

After successful payment:

* Invoice is generated automatically.
* Invoice displays:

  * Customer Information
  * Ordered Products
  * Quantity
  * Price
  * Total Amount
  * Payment ID
  * Order Date
* PDF generated using **xhtml2pdf**.

---

# 📦 Order Management

Users can

* Place Orders
* View Order History
* View Order Details
* Download Invoice
* View Payment Status

---

# 📧 Email Services

SMTP Mail is used for

* Registration OTP
* Password Reset OTP
* Email Verification

---

# 🔐 Security Features

* OTP Authentication
* Password Encryption
* Session Management
* Login Protection
* Secure Payment Verification
* Form Validation
* File Upload Validation

---

# ⚙️ Installation

## Clone Repository

```bash
git clone <repository-url>
```

## Navigate

```bash
cd Smart-cart-version-1-main
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Database Configuration

Configure your MySQL database inside **config.py**

Update

* Host
* Username
* Password
* Database Name

---

# Configure SMTP

Add

* Email Address
* Email Password

inside config.py

---

# Configure Razorpay

Add

* Razorpay Key ID
* Razorpay Secret Key

inside config.py

---

# Run Application

```bash
python app.py
```

Application URL

```
http://127.0.0.1:5000
```

---

# Complete Project Workflow

```
User Registration
        │
        ▼
OTP Verification
        │
        ▼
User Login
        │
        ▼
Browse Products
        │
        ▼
Product Details
        │
        ▼
Add To Cart
        │
        ▼
Address
        │
        ▼
Checkout
        │
        ▼
Razorpay Payment
        │
        ▼
Payment Success
        │
        ▼
Generate Invoice
        │
        ▼
My Orders
```

---

# Admin Workflow

```
Admin Signup
      │
      ▼
OTP Verification
      │
      ▼
Admin Login
      │
      ▼
Dashboard
      │
      ▼
Manage Products
      │
      ├── Add Product
      ├── View Products
      ├── Update Product
      └── Delete Product
```

---

# Future Enhancements

* Wishlist Module
* Product Reviews
* Product Ratings
* Coupon System
* Order Cancellation
* Return & Refund
* Admin Sales Analytics
* Stock Alerts
* SMS Notifications
* Multi-Vendor Marketplace
* AI Product Recommendations

---

# Author

**Chinni Yugandhar**

Bachelor of Technology (Electronics and Communication Engineering)

Python Full Stack Developer

---

# License

This project is developed for educational purposes and learning Flask Full Stack Development.
