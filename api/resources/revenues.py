from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import RevenueModel, AccountModel
from schemas import RevenueSchema, RevenueUpdateSchema

blp = Blueprint("revenues", __name__, description="Operations on revenues")

@blp.route("/revenue/<int:rev_id>")
class Revenue(MethodView):
    @jwt_required()
    @blp.response(200, RevenueSchema)
    def get(self, rev_id):
        acc_id = get_jwt_identity()
        revenue = RevenueModel.query.get_or_404(rev_id)
        if not revenue.account_id == acc_id:
            abort(409, message="Revenue does not belong to account")
        return revenue
    
    @jwt_required()
    @blp.arguments(RevenueUpdateSchema)
    @blp.response(200, RevenueSchema)
    def put(self, rev_data, rev_id):
        acc_id = get_jwt_identity()
        revenue = RevenueModel.query.get_or_404(rev_id)
        if not revenue.account_id == acc_id:
            abort(409, message="Revenue does not belong to account")

        if revenue:
            revenue.name = rev_data["name"]
            revenue.description = rev_data["description"]
            revenue.type = rev_data["type"]
            revenue.amount = rev_data["amount"]
            revenue.category_id = rev_data["category_id"]

        db.session.add(revenue)
        db.session.commit()

        return revenue
    
    def delete(self, rev_id):
        acc_id = get_jwt_identity()
        revenue = RevenueModel.query.get_or_404(rev_id)
        if not revenue.account_id == acc_id:
            abort(409, message="Revenue does not belong to account")
            
        db.session.delete(revenue)
        db.session.commit()
        return {"message": "Revenue successfully deleted"}

@blp.route("/revenue")
class RevenueList(MethodView):
    @jwt_required()
    @blp.response(200, RevenueSchema(many=True))
    def get(self):
        acc_id = get_jwt_identity()
        return RevenueModel.query.filter(RevenueModel.account_id == acc_id).all()
    
    @jwt_required()
    @blp.arguments(RevenueSchema)
    @blp.response(201, RevenueSchema)
    def post(self, rev_data):
        acc_id = get_jwt_identity()
        revenue = RevenueModel(account_id=acc_id, **rev_data)

        try:
            db.session.add(revenue)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error whilst inserting revenue into database")

        return revenue
