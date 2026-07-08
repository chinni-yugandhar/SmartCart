# config.py
# ------------------------------------
# This file holds all configurations
# like Secret Key, Database connection
# details, Email settings, Razorpay keys etc.
# Utilizes environment variables with local fallbacks.
# ------------------------------------

import os

SECRET_KEY = os.environ.get("SECRET_KEY", "abc@123")

# MySQL Database
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "Chinni@421")
DB_NAME = os.environ.get("DB_NAME", "smartcart_db")

# Email SMTP Settings
MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True").lower() == "true"
MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "chinniyugandhar996@gmail.com")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "pktt qwjx atsr giul")   # Gmail App Password

# Create Razorpay Config in config.py
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "rzp_test_T8arDbCRecREpU")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "l0DxBaC1TOklbgulP7b4SXgD")
