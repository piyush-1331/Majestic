from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# Secret key required for Flask session-based flash messaging
app.secret_key = "majestic_interior_furniture_pbl_secret_key"

# Route for Home page
@app.route("/")
@app.route("/home")
@app.route("/index")
@app.route("/index.html")
def home():
    return render_template("index.html")

# Route for About Us page
@app.route("/about")
@app.route("/about.html")
def about():
    return render_template("about.html")

# Route for Blog page
@app.route("/blog")
@app.route("/blog.html")
def blog():
    return render_template("blog.html")

# Route for Contact Us page
@app.route("/contact")
@app.route("/contact.html")
def contact():
    return render_template("contact.html")

# Route for Gallery page
@app.route("/gallery")
@app.route("/gallery.html")
def gallery():
    return render_template("gallery.html")

# Route for Pages (Typography & Components) page
@app.route("/pages")
@app.route("/pages.html")
def pages():
    return render_template("pages.html")

# Route for Single Blog Post page
@app.route("/single")
@app.route("/single.html")
def single():
    return render_template("single.html")

# Route for User Registration page (Task 2)
@app.route("/register", methods=["GET", "POST"])
@app.route("/register.html", methods=["GET", "POST"])
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
            flash(f"Registration successful for {name}! Please login with your credentials.", "success")
            return redirect(url_for("login"))

        return render_template("register.html", name=name, email=email, phone=phone)

    return render_template("register.html")

# Route for User Login page (Task 2)
@app.route("/login", methods=["GET", "POST"])
@app.route("/login.html", methods=["GET", "POST"])
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
            flash(f"Login successful! Welcome back, {email}.", "success")
            return render_template("login.html", email=email, login_success=True)

        return render_template("login.html", email=email)

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
