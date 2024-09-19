from flask import Flask, request
from flask_smorest import abort  # calls flask's abort method
from db import accounts, revenues, categories
import uuid

app = Flask(__name__)


### Account ###
@app.get("/account")
def get_all_accounts():
    return {"accounts" : list(accounts.items())}


@app.get("/account/<string:acc_id>")
def get_account(acc_id):
    try:
        return accounts[acc_id]
    except KeyError:
        abort(404, message="Account not found")  # documents in smorest


@app.post("/account")
def create_account():
    # TODO: validation that the payload is as expected
    acc_data = request.get_json()
    acc_id = uuid.uuid4().hex
    account = {**acc_data, "id": acc_id}
    accounts[acc_id] = account

    return account, 201


@app.put("/account/<string:acc_id>")
def update_account(acc_id):
    acc_data = request.get_json()
    try:
        account = accounts[acc_id]
        account |= acc_data
        return {"message": "Account updated"}
    except KeyError:
        abort(404, message="Account not found")


@app.delete("/account/<string:acc_id>")
def delete_account(acc_id):
    try:
        del accounts[acc_id]
        return {"message": "Account deleted"}
    except KeyError:
        abort(404, message="Account not found")


### Revenues ###
@app.get("/revenue")
def get_all_revenues():
    return {"revenues": list(revenues.items())}


@app.get("/revenue/<string:rev_id>")
def get_revenue(rev_id):
    try:
        return revenues[rev_id], 200
    except KeyError:
        abort(404, message="Revenue not found")


@app.post("/revenue")
def create_revenue():
    # TODO: validation that the payload is as expected
    rev_data = request.get_json()
    rev_id = uuid.uuid4().hex
    revenue = {**rev_data, "id": rev_id}
    revenues[rev_id] = revenue

    return revenue, 201


@app.put("/revenue/<string:rev_id>")
def update_revenue(rev_id):
    rev_data = request.get_json()
    try:
        revenue = revenues[rev_id]
        revenue |= rev_data
        return {"message": "Revenue updated"}
    except KeyError:
        abort(404, message="Revenue not found")


@app.delete("/revenue/<string:rev_id>")
def delete_revenue(rev_id):
    try:
        del revenues[rev_id]
        return {"message": "Revenue deleted"}
    except KeyError:
        abort(404, message="Revenue not found")


### Category ###
@app.get("/category")
def get_all_categories():
    return {"categorys": list(categories.items())}


@app.get("/category/<string:cat_id>")
def get_category(cat_id):
    try:
        return categories[cat_id], 200
    except KeyError:
        abort(404, message="Category not found")


@app.post("/category")
def create_category():
    # TODO: validation that the information is as expected
    cat_data = request.get_json()
    cat_id = uuid.uuid4().hex
    category = {**cat_data, "id": cat_id}
    categories[cat_id] = category
    return category, 201


@app.put("/category/<string:cat_id>")
def update_category(cat_id):
    cat_data = request.get_json()
    try:
        category = categories[cat_id]
        category |= cat_data
        return {"message": "Category updated"}
    except KeyError:
        abort(404, message="Category not found")


@app.delete("/category/<string:cat_id>")
def delete_category(cat_id):
    try:
        del categories[cat_id]
        return {"message": "Category deleted"}
    except KeyError:
        abort(404, message="Category not found")