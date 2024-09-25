import uuid, datetime
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import AccountModel
from schemas import AccountSchema, AccountUpdateSchema

blp = Blueprint("accounts", __name__, description="Operations on accounts")

@blp.route("/account/<string:acc_id>")
class Account(MethodView):
    @blp.response(200, AccountSchema)
    def get(self, acc_id):
        account = AccountModel.query.get_or_404(acc_id)
        return account

    @blp.arguments(AccountUpdateSchema)
    @blp.response(201, AccountSchema)
    def put(self, acc_data, acc_id):
        account = AccountModel.query.get_or_404(acc_id)

        if account:
            account.name = acc_data["name"]
            account.password = acc_data["password"]
            account.balance = acc_data["balance"]
        
        db.session.add(account)
        db.session.commit()

        return account

    def delete(self, acc_id):
        account = AccountModel.query.get_or_404(acc_id)
        raise NotImplementedError("Deleting an account is not implemented.")


@blp.route("/account")
class AccountList(MethodView):
    @blp.response(200, AccountSchema(many=True))
    def get(self):
        return accounts.values()

    @blp.arguments(AccountSchema)
    @blp.response(201, AccountSchema)
    def post(self, acc_data):
        account = AccountModel(**acc_data)

        try:
            db.session.add(account)
            db.session.commit()
        except IntegrityError:
            abort(400, message="An account using that email already exists")
        except SQLAlchemyError:
            abort(500, message="An error occurred whilst inserting the account")

        return account