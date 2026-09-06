from flask import Flask, render_template, request, redirect, url_for, flash
from db import client, expenses_collection
from datetime import datetime
from bson.objectid import ObjectId
app = Flask(__name__)
app.secret_key = "mysecretkey"

@app.route("/")
def home():
    category = request.args.get("category")
    search = request.args.get("search")

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    query = {}

    if search:
        query["item"] = {
            "$regex": search,
            "$options": "i"
        }
    if category:
        query["category"] = {
        "$eq": category
    } 
    if start_date and end_date:
        query["date"] = {
        "$gte": start_date,
        "$lte": end_date
    }
    
    expenses =  list(expenses_collection.find(query))
    
    # []
    total = 0
    monthly_total = 0
    today =datetime.now()
    current_month =today.month
    current_year = today.year

    pipeline = [
    {
        "$match": {
            "date": {
                "$regex": f"^{current_year}-{current_month:02d}"
            }
        }
    },
    {
        "$group": {
            "_id": None,
            "total": {"$sum": "$price"}
        }
    }
    ]

    result = list(expenses_collection.aggregate(pipeline)) 
    monthly_total = result[0]["total"] if result else 0
    for expense in expenses:
        total += expense["price"]
    total_entries = len(expenses)
    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        total_entries=total_entries,
        monthly_total=monthly_total
    )

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
    category = request.form["category"]
    if item == "":
        flash("Item cannot be empty")
        return redirect(url_for("home"))
    if date == "":
        flash("Date is required")
        return redirect(url_for("home"))
        return "Date is required"
    if price <= 0:
        flash("Price must be greater than 0")
        return redirect(url_for("home"))
    expense = {
        "date": date,
        "price": price,
        "item": item,
        "category": category
    }
    result = expenses_collection.insert_one(expense)
    expense["_id"] = result.inserted_id

    return render_template("expense_row.html", expense=expense)

@app.route("/edit/<expense_id>", methods =["GET", "POST"])
def edit_expense(expense_id):
    if request.method == "GET":
        expense = expenses_collection.find_one(
            {"_id": ObjectId(expense_id)}
        )
        return render_template(
            "edit_row.html",
            expense=expense
        )

    # POST - Save the edited expense

    date = request.form["date"]
    price = float(request.form["price"])
    item = request.form["item"]
    category = request.form["category"]

    expenses_collection.update_one(
        {"_id": ObjectId(expense_id)},
        {
            "$set": {
                "date": date,
                "price": price,
                "item": item,
                "category": category
            }
        }
    )
    expense = expenses_collection.find_one(
    {"_id": ObjectId(expense_id)}
    )
    # Return only the updated row
    return render_template(
    "expense_row.html",
    expense=expense
)


@app.route("/delete/<expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    expenses_collection.delete_one(
        {"_id": ObjectId(expense_id)}
    )
    return ""

# @app.route("/migrate-categories")
#def migrate_categories():
#   expenses_collection.update_many(
#       {"category": {"$exists": False}},
#       {"$set": {"category": "Other"}}
#
#    return "Old expenses migrated successfully!"

if __name__ == "__main__":
    app.run(debug=True)