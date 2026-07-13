
from dotenv import load_dotenv
load_dotenv()

import os


SECRET_KEY = os.environ.get("SECRET_KEY", "abc@123")

# MySQL Database
DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = int(os.environ.get("DB_PORT", 32226))

# Email SMTP Settings (Brevo)

MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp-relay.brevo.com")
MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True").lower() == "true"

MAIL_USERNAME = os.environ.get("MAIL_USERNAME")  # Brevo SMTP Login
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")  # Brevo SMTP Key
MAIL_SENDER = os.environ.get("MAIL_SENDER")      # Verified sender email
# Razorpay
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET")