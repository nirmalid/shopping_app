from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

USERS = {
    "shon": {"password": "shon123", "role": "user"},
    "nimi": {"password": "nimi123", "role": "admin"}
}

PRODUCTS = {
    101:{"name": "Boots", "price": 1999, "category_id": 1},
    102:{"name":"Sneakers", "price": 2499, "category_id": 1},
    201:{"name": "Dress", "price": 3499, "category_id": 2}
}

@app.route("/")
def home():
    username = "Nimi"
    return render_template("home.html", name = username)

@app.route("/catalog")
def catalog():
    return render_template("catalog.html", products = PRODUCTS)

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = USERS.get(username)

        if not user:
            flash("usrname does not exist.")
        elif user["password"] != password:
            flash("Incorrect password.")
        else:
            session["username"] = username
            session["role"] = user["role"]
            return redirect(url_for("catalog"))
    return render_template("login.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in USERS:
            flash("username already exists. Please choose a different one.")
            return redirect(url_for("register"))
        
        USERS[username] = password
        flash("Registration successful! You can now log in.")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/add_to_cart/<int:product_id>", methods = ["POST"])
def add_to_cart(product_id):
    if "cart" not in session:
        session["cart"] = []
    
    session["cart"].append(product_id)
    flash("Product added to cart!")
    return redirect(url_for("catalog"))

@app.route("/cart")
def cart():
    if "cart" not in session:
        session["cart"] = []
    
    cart_items = []
    for pid in session["cart"]:
        product = PRODUCTS.get(pid)
        if product:
            cart_items.append(product)
    
    return render_template("cart.html", cart_items = cart_items)
if __name__ == "__main__":
    app.run(debug=True)
