from flask import Flask, render_template, request, redirect, url_for
from db import client, expenses_collection
from datetime import datetime
app = Flask(__name__)

@app.route("/")
def home():
    expenses = expenses_collection.find()
    return render_template("index.html", expenses=expenses)

@app.route("/test-db")
def test_db():
    try:
        client.admin.command("ping")
        return "MongoDB Connected Successfully!"

    except Exception as e:
        import traceback
        return f"<pre>{traceback.format_exc()}</pre>"


@app.route("/add", methods=["POST"])
def add_expense():
    date = request.form["date"]
    price = float(request.form["price"])   
    item = request.form["item"]   
    expense = {
        "date": date,
        "price": price,
        "item": item,
    }
    expenses_collection.insert_one(expense)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)