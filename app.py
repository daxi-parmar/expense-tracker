from flask import Flask, render_template, request, redirect, url_for
from db import client, expenses_collection

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test-db")
def test_db():
    try:
        # Ping MongoDB server
        client.admin.command("ping")

        # Optional: Insert a test document
        expenses_collection.insert_one({
            "message": "MongoDB Connected Successfully!"
        })
        return " MongoDB Connected Successfully!"

    except Exception as e:
        return f" Connection Failed: {e}"

@app.route("/add", methods=["POST"])
def add_expense():
    date = request.form["date"]
    price = float(request.form["price"])   
    item = request.form["item"]   

    expense = {
        "date": date,
        "price": price,
        "item": item
    }
    expenses_collection.insert_one(expense)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)