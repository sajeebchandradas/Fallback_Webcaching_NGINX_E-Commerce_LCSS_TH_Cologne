from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Define absolute path for the database file in the same folder as app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data.db")

# Products List
products = [
    {"id": 1, "name": "Laptop", "price": "$799", "image": "laptop.jpg"},
    {"id": 2, "name": "Smartphone", "price": "$499", "image": "smartphone.jpg"},
    {"id": 3, "name": "Headphones", "price": "$99", "image": "headphones.jpg"},
    {"id": 4, "name": "Keyboard", "price": "$49", "image": "keyboard.jpg"},
    {"id": 5, "name": "Watch", "price": "$149", "image": "watch.jpg"},
    {"id": 6, "name": "Tablet", "price": "$299", "image": "tablet.jpg"}
]

# Create database and orders table
def init_db():
    print(f"🔧 Initializing database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            email TEXT,
            quantity INTEGER,
            address TEXT,
            payment_method TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template("index.html", products=products)

@app.route('/buy/<int:product_id>')
def buy(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    return render_template("buy.html", product=product)

@app.route('/submit_order', methods=["POST"])
def submit_order():
    product_name = request.form['product_name']
    email = request.form['email']
    quantity = request.form['quantity']
    address = request.form['address']
    payment_method = request.form['payment_method']

    print(f"💾 Saving order to: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO orders (product_name, email, quantity, address, payment_method) VALUES (?, ?, ?, ?, ?)",
              (product_name, email, quantity, address, payment_method))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)