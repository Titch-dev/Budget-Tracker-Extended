import uuid, datetime
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import accounts
from schemas import AccountSchema, AccountUpdateSchema

blp = Blueprint("accounts", __name__, description="Operations on accounts")

@blp.route("/account/<string:acc_id>")
class Account(MethodView):
    @blp.response(200, AccountSchema)
    def get(self, acc_id):
        try:
            return accounts[acc_id]
        except KeyError:
            abort(404, message="Account not found")

    @blp.arguments(AccountUpdateSchema)
    @blp.response(201, AccountSchema)
    def put(self, acc_data, acc_id):
        try:
            account = accounts[acc_id]
            account |= acc_data
            return account
        except KeyError:
            abort(404, message="Account not found")

    def delete(self, acc_id):
        try:
            del accounts[acc_id]
            return {"message": "Account deleted"}
        except KeyError:
            abort(404, message="Account not found")


@blp.route("/account/")
class AccountList(MethodView):
    @blp.response(200, AccountSchema(many=True))
    def get(self):
        return accounts.values()

    @blp.arguments(AccountSchema)
    @blp.response(201, AccountSchema)
    def post(self, acc_data):
        for account in accounts.values():
            if account["email"] == acc_data["email"]:
                abort(400, message="Account already exists")
        acc_id = uuid.uuid4().hex
        acc_created = datetime.datetime.now()
        account = {**acc_data, "id": acc_id, "created": acc_created}
        accounts[acc_id] = account

        return account