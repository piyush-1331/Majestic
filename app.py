import os
import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
    username = (os.getenv("SMTP_USERNAME") or os.getenv("MAIL_USERNAME") or "").strip()
    raw_password = os.getenv("SMTP_PASSWORD") or os.getenv("MAIL_PASSWORD") or ""
    # Strip spaces in case Google 16-character App Password was copied with spaces (e.g. 'abcd efgh ijkl mnop')
    password = raw_password.replace(" ", "").strip()
    sender = os.getenv("SMTP_SENDER") or os.getenv("MAIL_SENDER") or (
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
            # Task 3 Requirement: Redirect to Home after registration
            return redirect(url_for("home"))

        return render_template("register.html", name=name, email=email, phone=phone)

    return render_template("register.html")

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
                return redirect(url_for("home"))
            else:
                # Invalid Credentials Flow (wrong password or unregistered email):
                # 1. Send "Login Failed" email to the entered email address
                # 2. Show error message on the Login page
                send_login_failed_email(email)
                flash("Invalid email or password. A security alert email has been sent to the entered address.", "error")
                return render_template("login.html", email=email)

        return render_template("login.html", email=email)

    return render_template("login.html")

# Route for User Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

