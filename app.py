import os
import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import razorpay
from dotenv import load_dotenv

from flask import Flask, render_template, request, redirect, url_for, flash, session

# Load environment variables from .env file
load_dotenv()


app = Flask(__name__)
# Secret key required for Flask session-based flash messaging
app.secret_key = os.getenv("SECRET_KEY", "majestic_interior_furniture_pbl_secret_key")

# Path to the JSON data file for storing registered users
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "users.json")

def load_users():
    """Load registered users list from data/users.json."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_users(users):
    """Save registered users list to data/users.json."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

# ==============================================================================
# Task 4: SMTP Email Notification System
# ==============================================================================

def get_smtp_config():
    """Retrieve SMTP configuration dynamically from environment variables (.env)."""
    load_dotenv(override=False)
    server = (os.getenv("SMTP_SERVER") or os.getenv("MAIL_SERVER") or "smtp.gmail.com").strip()
    port_str = os.getenv("SMTP_PORT") or os.getenv("MAIL_PORT") or "587"
    try:
        port = int(port_str.strip())
    except ValueError:
        port = 587
    use_tls_str = os.getenv("SMTP_USE_TLS") or os.getenv("MAIL_USE_TLS") or "True"
    use_tls = use_tls_str.strip().lower() in ("true", "1", "yes")
    username = (os.getenv("MAIL_USERNAME") or os.getenv("SMTP_USERNAME") or "").strip()
    raw_password = os.getenv("MAIL_PASSWORD") or os.getenv("SMTP_PASSWORD") or ""
    # Strip spaces in case Google 16-character App Password was copied with spaces (e.g. 'abcd efgh ijkl mnop')
    password = raw_password.replace(" ", "").strip()
    sender = os.getenv("MAIL_SENDER") or os.getenv("SMTP_SENDER") or (
        f"Majestic Interior & Furniture <{username}>" if username else "noreply@majesticinterior.com"
    )
    return {
        "server": server,
        "port": port,
        "use_tls": use_tls,
        "username": username,
        "password": password,
        "sender": sender
    }

def send_email_notification(recipient_email, subject, text_body, html_body=None):
    """
    Sends an email notification via SMTP using configuration from environment variables (.env).
    Gracefully handles missing configuration or connection errors.
    Returns (success: bool, info: str).
    """
    config = get_smtp_config()

    # If credentials are not configured or set to placeholder, log a simulation message
    if not config["username"] or not config["password"] or config["username"] == "your_email@gmail.com":
        simulated_info = (
            f"[SMTP Simulation] No active credentials in .env. "
            f"Email simulated for '{recipient_email}' | Subject: '{subject}'"
        )
        print(simulated_info)
        return True, simulated_info

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = config["sender"]
        msg["To"] = recipient_email

        # Attach plain-text fallback
        msg.attach(MIMEText(text_body, "plain", "utf-8"))

        # Attach HTML version if provided
        if html_body:
            msg.attach(MIMEText(html_body, "html", "utf-8"))

        with smtplib.SMTP(config["server"], config["port"], timeout=10) as server:
            if config["use_tls"]:
                server.starttls()
            server.login(config["username"], config["password"])
            server.send_message(msg)

        success_info = f"[SMTP Success] Email delivered to {recipient_email} ('{subject}')"
        print(success_info)
        return True, success_info
    except Exception as e:
        error_info = f"[SMTP Warning] Delivery to {recipient_email} failed: {e}"
        print(error_info)
        return False, error_info

def send_login_success_email(user_email, user_name):
    """Sends a 'Login Successful' notification to the registered user."""
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    subject = "Majestic Interior — Login Successful"

    text_body = f"""Hello {user_name},

You have successfully logged in to your Majestic Interior & Furniture account.

Login Details:
- Registered Account: {user_email}
- Date & Time: {timestamp}
- Status: Authenticated Successfully

If you did not initiate this login, please secure your account immediately.

Warm regards,
Majestic Interior & Furniture Team
"""

    html_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #f7f7f7; margin: 0; padding: 20px; }}
    .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 8px; overflow: hidden; border: 1px solid #e0e0e0; }}
    .header {{ background: #97262A; color: #ffffff; padding: 24px; text-align: center; }}
    .header h1 {{ margin: 0; font-size: 22px; font-weight: 600; letter-spacing: 1px; }}
    .content {{ padding: 28px; color: #333333; line-height: 1.6; font-size: 15px; }}
    .badge {{ display: inline-block; background: #e8f5e9; color: #2e7d32; font-weight: bold; padding: 6px 14px; border-radius: 4px; font-size: 13px; margin: 10px 0; }}
    .details {{ background: #fafafa; border-left: 4px solid #97262A; padding: 14px 18px; margin: 18px 0; border-radius: 0 4px 4px 0; }}
    .footer {{ background: #f0f0f0; padding: 16px; text-align: center; font-size: 12px; color: #777777; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>MAJESTIC INTERIOR &amp; FURNITURE</h1>
    </div>
    <div class="content">
      <p>Hello <strong>{user_name}</strong>,</p>
      <div class="badge">&#10004; Login Successful</div>
      <p>You have successfully logged in to your Majestic Interior &amp; Furniture account.</p>
      <div class="details">
        <p style="margin: 4px 0;"><strong>Registered Account:</strong> {user_email}</p>
        <p style="margin: 4px 0;"><strong>Date &amp; Time:</strong> {timestamp}</p>
        <p style="margin: 4px 0;"><strong>Status:</strong> Authenticated Successfully</p>
      </div>
      <p style="font-size: 13px; color: #666666;">If you did not perform this login, please contact our support team or secure your credentials immediately.</p>
    </div>
    <div class="footer">
      &copy; Majestic Interior &amp; Furniture. All rights reserved.
    </div>
  </div>
</body>
</html>
"""
    return send_email_notification(user_email, subject, text_body, html_body)

def send_login_failed_email(entered_email):
    """Sends a 'Login Failed' security alert to the entered email address."""
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    subject = "Security Alert: Unsuccessful Login Attempt — Majestic Interior"

    text_body = f"""Security Alert: Unsuccessful Login Attempt

An unsuccessful login attempt was detected on Majestic Interior & Furniture using this email address: {entered_email}.

Attempt Details:
- Attempted Account: {entered_email}
- Date & Time: {timestamp}
- Status: Failed (Invalid Credentials)

If you attempted to sign in and forgot your password, please verify your credentials or register an account.
If you did not initiate this attempt, please be advised that someone entered your email on our login page.

Warm regards,
Majestic Interior & Furniture Security Team
"""

    html_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #f7f7f7; margin: 0; padding: 20px; }}
    .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 8px; overflow: hidden; border: 1px solid #e0e0e0; }}
    .header {{ background: #97262A; color: #ffffff; padding: 24px; text-align: center; }}
    .header h1 {{ margin: 0; font-size: 22px; font-weight: 600; letter-spacing: 1px; }}
    .content {{ padding: 28px; color: #333333; line-height: 1.6; font-size: 15px; }}
    .badge {{ display: inline-block; background: #ffebee; color: #c62828; font-weight: bold; padding: 6px 14px; border-radius: 4px; font-size: 13px; margin: 10px 0; }}
    .details {{ background: #fafafa; border-left: 4px solid #c62828; padding: 14px 18px; margin: 18px 0; border-radius: 0 4px 4px 0; }}
    .footer {{ background: #f0f0f0; padding: 16px; text-align: center; font-size: 12px; color: #777777; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>MAJESTIC INTERIOR &amp; FURNITURE</h1>
    </div>
    <div class="content">
      <div class="badge">&#9888; Unsuccessful Login Attempt</div>
      <p>An unsuccessful attempt to log in to <strong>Majestic Interior &amp; Furniture</strong> was detected using this email address.</p>
      <div class="details">
        <p style="margin: 4px 0;"><strong>Attempted Email:</strong> {entered_email}</p>
        <p style="margin: 4px 0;"><strong>Date &amp; Time:</strong> {timestamp}</p>
        <p style="margin: 4px 0;"><strong>Status:</strong> Failed (Invalid Credentials)</p>
      </div>
      <p style="font-size: 13px; color: #666666;">If you attempted to sign in, please check your credentials or register an account. If this was not you, someone may have mistyped their email address.</p>
    </div>
    <div class="footer">
      &copy; Majestic Interior &amp; Furniture Security. All rights reserved.
    </div>
  </div>
</body>
</html>
"""
    return send_email_notification(entered_email, subject, text_body, html_body)

def send_registration_success_email(user_email, user_name):
    """Sends a 'Registration Successful' welcome email to the newly registered user."""
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    subject = "Welcome to Majestic Interior & Furniture — Registration Successful"

    text_body = f"""Hello {user_name},

Welcome to Majestic Interior & Furniture!

Your account has been registered successfully.

Account Details:
- Name: {user_name}
- Registered Email: {user_email}
- Date & Time: {timestamp}
- Status: Account Activated

You can now log in to explore our luxury interior designs, custom furniture catalogues, and exclusive member consultations.

Warm regards,
Majestic Interior & Furniture Team
"""

    html_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #f7f7f7; margin: 0; padding: 20px; }}
    .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 8px; overflow: hidden; border: 1px solid #e0e0e0; }}
    .header {{ background: #97262A; color: #ffffff; padding: 24px; text-align: center; }}
    .header h1 {{ margin: 0; font-size: 22px; font-weight: 600; letter-spacing: 1px; }}
    .content {{ padding: 28px; color: #333333; line-height: 1.6; font-size: 15px; }}
    .badge {{ display: inline-block; background: #e8f5e9; color: #2e7d32; font-weight: bold; padding: 6px 14px; border-radius: 4px; font-size: 13px; margin: 10px 0; }}
    .details {{ background: #fafafa; border-left: 4px solid #97262A; padding: 14px 18px; margin: 18px 0; border-radius: 0 4px 4px 0; }}
    .footer {{ background: #f0f0f0; padding: 16px; text-align: center; font-size: 12px; color: #777777; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>MAJESTIC INTERIOR &amp; FURNITURE</h1>
    </div>
    <div class="content">
      <p>Hello <strong>{user_name}</strong>,</p>
      <div class="badge">&#10004; Registration Successful</div>
      <p>Welcome to <strong>Majestic Interior &amp; Furniture</strong>! Your account has been registered successfully.</p>
      <div class="details">
        <p style="margin: 4px 0;"><strong>Name:</strong> {user_name}</p>
        <p style="margin: 4px 0;"><strong>Registered Email:</strong> {user_email}</p>
        <p style="margin: 4px 0;"><strong>Registered Date:</strong> {timestamp}</p>
        <p style="margin: 4px 0;"><strong>Status:</strong> Active</p>
      </div>
      <p style="font-size: 13px; color: #666666;">You can now log in to save your favorite interior projects, request consultations, and explore customized furniture pieces.</p>
    </div>
    <div class="footer">
      &copy; Majestic Interior &amp; Furniture. All rights reserved.
    </div>
  </div>
</body>
</html>
"""
    return send_email_notification(user_email, subject, text_body, html_body)

def send_payment_success_email(user_email, user_name, amount, order_id, payment_id):
    """Sends a 'Payment Received Successfully' receipt email to the registered user."""
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    subject = f"Payment Successful (₹{amount}) — Majestic Interior & Furniture"

    text_body = f"""Hello {user_name},

Thank you! Your payment of ₹{amount} INR to Majestic Interior & Furniture has been successfully processed and cryptographically verified.

Transaction Receipt:
- Amount Paid: ₹{amount} INR
- Payment ID: {payment_id}
- Order ID: {order_id}
- Date & Time: {timestamp}
- Status: Completed & Verified (Razorpay Test Mode)

Our design and booking team has been notified and will proceed with your order details shortly.

Please keep this email for your transaction records. If you have any questions or require custom interior assistance, please reply directly to this email.

Warm regards,
Majestic Interior & Furniture Team
"""

    html_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #f7f7f7; margin: 0; padding: 20px; }}
    .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 8px; overflow: hidden; border: 1px solid #e0e0e0; }}
    .header {{ background: #97262A; color: #ffffff; padding: 24px; text-align: center; }}
    .header h1 {{ margin: 0; font-size: 22px; font-weight: 600; letter-spacing: 1px; }}
    .content {{ padding: 28px; color: #333333; line-height: 1.6; font-size: 15px; }}
    .badge {{ display: inline-block; background: #e8f5e9; color: #2e7d32; font-weight: bold; padding: 6px 14px; border-radius: 4px; font-size: 13px; margin: 10px 0; }}
    .amount-highlight {{ font-size: 28px; font-weight: 700; color: #97262A; margin: 12px 0; }}
    .details {{ background: #fafafa; border-left: 4px solid #2e7d32; padding: 14px 18px; margin: 18px 0; border-radius: 0 4px 4px 0; }}
    .details-table {{ width: 100%; border-collapse: collapse; margin-top: 8px; }}
    .details-table td {{ padding: 6px 0; font-size: 14px; }}
    .details-table td.label {{ color: #777777; width: 35%; }}
    .details-table td.val {{ color: #222222; font-weight: 600; }}
    .note-box {{ background: #fdfaf6; border: 1px solid #f0e6dc; padding: 12px 16px; border-radius: 4px; font-size: 13px; color: #6d4c41; margin-top: 18px; }}
    .footer {{ background: #f0f0f0; padding: 16px; text-align: center; font-size: 12px; color: #777777; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>MAJESTIC INTERIOR &amp; FURNITURE</h1>
    </div>
    <div class="content">
      <p>Hello <strong>{user_name}</strong>,</p>
      <div class="badge">&#10004; Payment Received Successfully</div>
      <div class="amount-highlight">₹{amount} <span style="font-size: 15px; color: #666; font-weight: normal;">INR</span></div>
      <p>Your test payment has been successfully processed and verified on our server via Razorpay.</p>
      <div class="details">
        <table class="details-table">
          <tr>
            <td class="label">Payment ID:</td>
            <td class="val"><code style="background: #e9ecef; padding: 2px 6px; border-radius: 3px;">{payment_id}</code></td>
          </tr>
          <tr>
            <td class="label">Order ID:</td>
            <td class="val"><code style="background: #e9ecef; padding: 2px 6px; border-radius: 3px;">{order_id}</code></td>
          </tr>
          <tr>
            <td class="label">Amount Paid:</td>
            <td class="val" style="color: #97262A; font-weight: 700;">₹{amount} INR</td>
          </tr>
          <tr>
            <td class="label">Date &amp; Time:</td>
            <td class="val">{timestamp}</td>
          </tr>
          <tr>
            <td class="label">Verification:</td>
            <td class="val" style="color: #2e7d32;">HMAC-SHA256 Signature Verified</td>
          </tr>
        </table>
      </div>
      <div class="note-box">
        <strong>Order Status:</strong> Our design &amp; booking team has received your order details and will be in touch shortly. Please keep this digital receipt for your reference.
      </div>
    </div>
    <div class="footer">
      &copy; Majestic Interior &amp; Furniture. All rights reserved.
    </div>
  </div>
</body>
</html>
"""
    return send_email_notification(user_email, subject, text_body, html_body)

def send_payment_failed_email(user_email, user_name, amount, order_id, reason):
    """Sends a 'Payment Incomplete or Cancelled' alert email to the customer."""
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    amount_display = f"₹{amount} INR" if amount and amount != "N/A" else "Payment Attempt"
    subject = f"Payment Incomplete ({amount_display}) — Majestic Interior"

    text_body = f"""Hello {user_name},

We noticed that your recent payment attempt on Majestic Interior & Furniture was not completed.

Attempt Details:
- Amount: {amount_display}
- Order ID: {order_id if order_id else 'N/A'}
- Reason: {reason}
- Date & Time: {timestamp}
- Status: Failed / Incomplete

Important Notice:
If any amount was debited from your bank account or card during this attempt, it will be automatically refunded by your banking partner within 3 to 5 business days according to standard banking regulations.

You can retry your transaction at any time by logging in to your Majestic Interior account.

Warm regards,
Majestic Interior & Furniture Support Team
"""

    html_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #f7f7f7; margin: 0; padding: 20px; }}
    .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 8px; overflow: hidden; border: 1px solid #e0e0e0; }}
    .header {{ background: #97262A; color: #ffffff; padding: 24px; text-align: center; }}
    .header h1 {{ margin: 0; font-size: 22px; font-weight: 600; letter-spacing: 1px; }}
    .content {{ padding: 28px; color: #333333; line-height: 1.6; font-size: 15px; }}
    .badge {{ display: inline-block; background: #ffebee; color: #c62828; font-weight: bold; padding: 6px 14px; border-radius: 4px; font-size: 13px; margin: 10px 0; }}
    .amount-highlight {{ font-size: 24px; font-weight: 700; color: #c62828; margin: 12px 0; }}
    .details {{ background: #fafafa; border-left: 4px solid #c62828; padding: 14px 18px; margin: 18px 0; border-radius: 0 4px 4px 0; }}
    .details-table {{ width: 100%; border-collapse: collapse; margin-top: 8px; }}
    .details-table td {{ padding: 6px 0; font-size: 14px; }}
    .details-table td.label {{ color: #777777; width: 35%; }}
    .details-table td.val {{ color: #222222; font-weight: 600; }}
    .help-box {{ background: #fff8e1; border: 1px solid #ffe082; padding: 12px 16px; border-radius: 4px; font-size: 13px; color: #795548; margin: 18px 0; }}
    .footer {{ background: #f0f0f0; padding: 16px; text-align: center; font-size: 12px; color: #777777; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>MAJESTIC INTERIOR &amp; FURNITURE</h1>
    </div>
    <div class="content">
      <p>Hello <strong>{user_name}</strong>,</p>
      <div class="badge">&#9888; Payment Incomplete or Cancelled</div>
      <div class="amount-highlight">{amount_display}</div>
      <p>Your recent payment attempt on Majestic Interior &amp; Furniture was not completed.</p>
      <div class="details">
        <table class="details-table">
          <tr>
            <td class="label">Order ID:</td>
            <td class="val"><code style="background: #e9ecef; padding: 2px 6px; border-radius: 3px;">{order_id if order_id else 'N/A'}</code></td>
          </tr>
          <tr>
            <td class="label">Reason:</td>
            <td class="val" style="color: #c62828;">{reason}</td>
          </tr>
          <tr>
            <td class="label">Date &amp; Time:</td>
            <td class="val">{timestamp}</td>
          </tr>
          <tr>
            <td class="label">Status:</td>
            <td class="val" style="color: #c62828;">Failed / Cancelled</td>
          </tr>
        </table>
      </div>
      <div class="help-box">
        <strong>Automatic Refund Assurance:</strong> If any amount was debited from your card, UPI or bank account, it will automatically be refunded back to your original source of payment within 3-5 business days.
      </div>
      <p style="font-size: 13px; color: #666666;">You can log in to your account and try again whenever you are ready.</p>
    </div>
    <div class="footer">
      &copy; Majestic Interior &amp; Furniture Support. All rights reserved.
    </div>
  </div>
</body>
</html>
"""
    return send_email_notification(user_email, subject, text_body, html_body)

# Context processor to make current_user available in all templates
@app.context_processor
def inject_user():
    return dict(current_user=session.get("user"))


# Route for Home page (Task 1 & Task 3: passes registered users to template)

@app.route("/index.html")
@app.route("/index")
@app.route("/home")
@app.route("/")
def home():
    users = load_users()
    return render_template("index.html", users=users)

# Route for About Us page
@app.route("/about.html")
@app.route("/about")
def about():
    return render_template("about.html")

# Route for Blog page
@app.route("/blog.html")
@app.route("/blog")
def blog():
    return render_template("blog.html")

# Route for Contact Us page
@app.route("/contact.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")

# Route for Gallery page
@app.route("/gallery.html")
@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

# Route for Pages (Typography & Components) page
@app.route("/pages.html")
@app.route("/pages")
def pages():
    return render_template("pages.html")

# Route for Single Blog Post page
@app.route("/single.html")
@app.route("/single")
def single():
    return render_template("single.html")

# Route for User Registration page (Task 2 & Task 3)
@app.route("/register.html", methods=["GET", "POST"])
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Server-side validation
        if not name:
            flash("Full Name is required.", "error")
        elif not email:
            flash("Email Address is required.", "error")
        elif not phone:
            flash("Phone Number is required.", "error")
        elif not password:
            flash("Password is required.", "error")
        elif not confirm_password:
            flash("Confirm Password is required.", "error")
        elif password != confirm_password:
            flash("Password and Confirm Password do not match.", "error")
        else:
            # Check for duplicate email registration
            users = load_users()
            email_exists = any(u.get("email", "").lower() == email.lower() for u in users)
            if email_exists:
                flash("Email already registered.", "error")
                return render_template("register.html", name=name, email=email, phone=phone)

            # Store the new registration record in data/users.json
            new_user = {
                "name": name,
                "email": email,
                "phone": phone,
                "password": password
            }
            users.append(new_user)
            save_users(users)

            # Send registration welcome email
            send_registration_success_email(email, name)

            # Establish session for logged-in user
            session["user"] = {
                "name": name,
                "email": email
            }

            flash(f"Registration successful for {name}! A welcome email has been sent to {email}.", "success")
            next_page = request.values.get("next", "").strip()
            if next_page in ("payment", "/payment", "payment.html", "/payment.html"):
                return redirect(url_for("payment"))
            return redirect(url_for("home"))

        next_url = request.values.get("next", "").strip()
        return render_template("register.html", name=name, email=email, phone=phone, next_url=next_url)

    next_url = request.args.get("next", "").strip()
    return render_template("register.html", next_url=next_url)

# Route for User Login page (Task 2 & Task 4)
@app.route("/login.html", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Server-side validation
        if not email:
            flash("Email Address is required.", "error")
        elif not password:
            flash("Password is required.", "error")
        else:
            users = load_users()
            user = next((u for u in users if u.get("email", "").lower() == email.lower()), None)

            # Task 4: Authenticate user credentials against registered records
            if user and user.get("password") == password:
                # Valid Credentials Flow:
                # 1. Authenticate user & set session
                # 2. Send "Login Successful" email to registered email
                # 3. Flash success message
                # 4. Redirect to home page
                user_email = user.get("email", email)
                user_name = user.get("name", "User")
                send_login_success_email(user_email, user_name)
                session["user"] = {
                    "name": user_name,
                    "email": user_email
                }
                flash(f"Login successful! Welcome back, {user_name}. A login confirmation email has been sent to {user_email}.", "success")
                next_page = request.values.get("next", "").strip()
                if next_page in ("payment", "/payment", "payment.html", "/payment.html"):
                    return redirect(url_for("payment"))
                return redirect(url_for("home"))
            else:
                # Invalid Credentials Flow (wrong password or unregistered email):
                # 1. Send "Login Failed" email to the entered email address
                # 2. Show error message on the Login page
                send_login_failed_email(email)
                flash("Invalid email or password. A security alert email has been sent to the entered address.", "error")
                next_url = request.values.get("next", "").strip()
                return render_template("login.html", email=email, next_url=next_url)

        next_url = request.values.get("next", "").strip()
        return render_template("login.html", email=email, next_url=next_url)

    next_url = request.args.get("next", "").strip()
    return render_template("login.html", next_url=next_url)

# Route for User Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("home"))

# ==============================================================================
# Task 5: Razorpay Payment Gateway Demonstration (Test Mode Only)
# ==============================================================================

def get_razorpay_client():
    """
    Retrieve and initialize the Razorpay Client dynamically using test keys from .env.
    Returns (client, key_id, key_secret).
    """
    load_dotenv(override=False)
    key_id = (os.getenv("RAZORPAY_KEY_ID") or "").strip()
    key_secret = (os.getenv("RAZORPAY_KEY_SECRET") or "").strip()

    if not key_id or not key_secret or key_id == "your_test_key_id":
        return None, key_id, key_secret

    try:
        client = razorpay.Client(auth=(key_id, key_secret))
        client.set_app_details({"title": "Majestic Interior PBL", "version": "1.0"})
        return client, key_id, key_secret
    except Exception as e:
        print(f"[Razorpay Init Error] {e}")
        return None, key_id, key_secret


@app.route("/payment.html", methods=["GET", "POST"])
@app.route("/payment", methods=["GET", "POST"])
def payment():
    # Require user login before making any payment
    user = session.get("user")
    if not user:
        flash("Please log in to your account to proceed with payment.", "error")
        return redirect(url_for("login", next="payment"))

    if request.method == "POST":
        amount_raw = request.form.get("amount", "").strip()
        customer_name = request.form.get("name", "").strip() or user.get("name", "Valued Customer")
        customer_email = request.form.get("email", "").strip() or user.get("email", "")

        # Server-side amount validation
        if not amount_raw:
            flash("Please enter a payment amount.", "error")
            return render_template("payment.html", amount=amount_raw)

        try:
            amount_val = float(amount_raw)
        except ValueError:
            flash("Amount must be a valid numeric value.", "error")
            return render_template("payment.html", amount=amount_raw)

        if amount_val <= 0:
            flash("Payment amount must be greater than zero.", "error")
            return render_template("payment.html", amount=amount_raw)

        # Convert to smallest currency unit (paise)
        amount_in_paise = int(round(amount_val * 100))
        if amount_in_paise < 100:
            flash("Minimum transaction amount is ₹1.00 (100 paise).", "error")
            return render_template("payment.html", amount=amount_raw)

        client, key_id, key_secret = get_razorpay_client()
        if not client:
            flash(
                "Razorpay Test Mode keys are not configured in .env. "
                "Please configure RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET to initiate live sandbox orders.",
                "error"
            )
            return render_template("payment.html", amount=amount_raw)

        try:
            # Server-side Razorpay Test Order Creation
            order_data = {
                "amount": amount_in_paise,
                "currency": "INR",
                "receipt": f"rcpt_majestic_{int(datetime.now().timestamp())}",
                "payment_capture": 1
            }
            razorpay_order = client.order.create(data=order_data)
            order_id = razorpay_order["id"]

            # Store order context in session for email notifications
            session["last_payment_amount"] = f"{amount_val:.2f}"
            session["last_order_customer_name"] = customer_name
            session["last_order_customer_email"] = customer_email

            return render_template(
                "payment.html",
                checkout_ready=True,
                order_id=order_id,
                key_id=key_id,
                amount=f"{amount_val:.2f}",
                amount_in_paise=amount_in_paise,
                currency="INR",
                customer_name=customer_name,
                customer_email=customer_email
            )
        except Exception as e:
            flash(f"Razorpay order creation failed: {str(e)}", "error")
            return render_template("payment.html", amount=amount_raw)

    return render_template("payment.html")


@app.route("/payment/success", methods=["GET", "POST"])
def payment_success():
    if request.method == "POST":
        payment_id = request.form.get("razorpay_payment_id", "").strip()
        order_id = request.form.get("razorpay_order_id", "").strip()
        signature = request.form.get("razorpay_signature", "").strip()
        amount = request.form.get("amount", "0.00").strip()

        user = session.get("user") or {}
        customer_email = request.form.get("email", "").strip() or user.get("email") or session.get("last_order_customer_email", "")
        customer_name = request.form.get("name", "").strip() or user.get("name") or session.get("last_order_customer_name", "Valued Customer")

        if not payment_id or not order_id or not signature:
            flash("Incomplete payment response received from checkout.", "error")
            return redirect(url_for("payment"))

        client, key_id, key_secret = get_razorpay_client()
        if not client:
            flash("Payment verification failed: Razorpay client is not configured.", "error")
            return redirect(url_for("payment"))

        try:
            # Server-side cryptographic signature verification using Razorpay SDK
            params_dict = {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            }
            client.utility.verify_payment_signature(params_dict)

            # Send Successful Payment Confirmation Email to user
            if customer_email:
                send_payment_success_email(
                    user_email=customer_email,
                    user_name=customer_name,
                    amount=amount,
                    order_id=order_id,
                    payment_id=payment_id
                )

            return render_template(
                "payment.html",
                payment_status="success",
                payment_id=payment_id,
                order_id=order_id,
                amount=amount,
                currency="INR",
                customer_name=customer_name,
                customer_email=customer_email,
                timestamp=datetime.now().strftime("%B %d, %Y at %I:%M %p")
            )
        except razorpay.errors.SignatureVerificationError:
            if customer_email:
                send_payment_failed_email(
                    user_email=customer_email,
                    user_name=customer_name,
                    amount=amount,
                    order_id=order_id,
                    reason="Signature verification failed. The payment response could not be verified by the backend."
                )
            return render_template(
                "payment.html",
                payment_status="failed",
                error_message="Signature verification failed. The payment response could not be verified by the backend.",
                order_id=order_id,
                amount=amount,
                customer_email=customer_email
            )
        except Exception as e:
            if customer_email:
                send_payment_failed_email(
                    user_email=customer_email,
                    user_name=customer_name,
                    amount=amount,
                    order_id=order_id,
                    reason=f"Verification error: {str(e)}"
                )
            return render_template(
                "payment.html",
                payment_status="failed",
                error_message=f"Verification error: {str(e)}",
                order_id=order_id,
                amount=amount,
                customer_email=customer_email
            )

    return redirect(url_for("payment"))


@app.route("/payment/failure", methods=["GET", "POST"])
def payment_failure():
    reason = request.values.get("reason", "Payment was cancelled or dismissed by user.")
    order_id = request.values.get("order_id", "")
    amount = request.values.get("amount", "") or session.get("last_payment_amount", "")

    user = session.get("user") or {}
    customer_email = user.get("email") or session.get("last_order_customer_email", "")
    customer_name = user.get("name") or session.get("last_order_customer_name", "Valued Customer")

    # Send failed/cancelled email alert (deduplicated per order attempt)
    last_alerted = session.get("last_failed_alert_order")
    if customer_email and order_id and last_alerted != order_id:
        session["last_failed_alert_order"] = order_id
        send_payment_failed_email(
            user_email=customer_email,
            user_name=customer_name,
            amount=amount or "N/A",
            order_id=order_id,
            reason=reason
        )

    return render_template(
        "payment.html",
        payment_status="failed",
        error_message=reason,
        order_id=order_id,
        amount=amount,
        customer_email=customer_email
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


