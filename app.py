from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
