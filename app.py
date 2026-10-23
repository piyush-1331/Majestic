import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# Secret key required for Flask session-based flash messaging
app.secret_key = "majestic_interior_furniture_pbl_secret_key"

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

            flash(f"Registration successful for {name}! Welcome to Majestic.", "success")
            # Task 3 Requirement: Redirect to Home after registration
            return redirect(url_for("home"))

        return render_template("register.html", name=name, email=email, phone=phone)

    return render_template("register.html")

# Route for User Login page (Task 2)
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
            if user:
                if user.get("password") == password:
                    flash(f"Login successful! Welcome back, {user.get('name', email)}.", "success")
                    return render_template("login.html", email=email, login_success=True)
                else:
                    flash("Invalid email or password.", "error")
                    return render_template("login.html", email=email)
            else:
                flash(f"Login successful! Welcome back, {email}.", "success")
                return render_template("login.html", email=email, login_success=True)

        return render_template("login.html", email=email)

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
