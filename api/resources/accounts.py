from datetime import datetime

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256

from db import db
from models import AccountModel
from schemas import AccountSchema, AccountUpdateSchema
from blocklist import BLOCKLIST

blp = Blueprint("accounts", __name__, description="Operations on accounts")

@blp.route("/account")
class AccountList(MethodView):
    @jwt_required()
    @blp.response(200, AccountSchema)
    def get(self):
        acc_id = get_jwt_identity()
        return AccountModel.query.get_or_404(acc_id)
    
    @jwt_required()
    @blp.arguments(AccountUpdateSchema)
    @blp.response(201, AccountSchema)
    def put(self, acc_data):
        acc_id = get_jwt_identity()
        account = AccountModel.query.get_or_404(acc_id)

        if account:
            account.name = acc_data["name"]
            account.password = pbkdf2_sha256.hash(acc_data["password"])
            account.balance = acc_data["balance"]
        
        db.session.add(account)
        db.session.commit()

        return account
    
    @jwt_required()
    def delete(self):
        acc_id = get_jwt_identity()
        account = AccountModel.query.get_or_404(acc_id)
        db.session.delete(account)
        db.session.commit()
        return {"message": "Account successfully deleted"}


@blp.route("/register")
class AccountRegister(MethodView):
    @blp.arguments(AccountSchema)
    def post(self, acc_data):
        account = AccountModel(name=acc_data["name"],
                               password=pbkdf2_sha256.hash(acc_data["password"]),
                               email=acc_data["email"])
        try:
            db.session.add(account)
            db.session.commit()
        except IntegrityError:
            abort(409, message="An account using that email already exists")
        except SQLAlchemyError:
            abort(500, message="An error occurred whilst inserting the account")

        return {"message" : "Account created successfully"}, 201
    

@blp.route("/login")
class AccountLogin(MethodView):
    @blp.arguments(AccountSchema)
    def post(self, acc_data):
        account = AccountModel.query.filter(
            AccountModel.email == acc_data["email"]
        ).first()

        if account and pbkdf2_sha256.verify(acc_data["password"], 
                                            account.password):
            access_token = create_access_token(identity=account.id)
            login = datetime.now()
            account.last_login = login
            db.session.add(account)
            db.session.commit()
                
            return {"access_token": access_token}
        
        abort(401, message="Invalid credentials")

@blp.route("/logout")
class AccountLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}
