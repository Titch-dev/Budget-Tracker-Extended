from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import RevenueModel
from schemas import RevenueSchema, RevenueUpdateSchema

blp = Blueprint("revenues", __name__, description="Operations on revenues")

@blp.route("/revenue/<string:rev_id>")
class Revenue(MethodView):
    @blp.response(200, RevenueSchema)
    def get(self, rev_id):
        revenue = RevenueModel.query.get_or_404(rev_id)
        return revenue
    
    @blp.arguments(RevenueUpdateSchema)
    @blp.response(201, RevenueSchema)
    def put(self, rev_data, rev_id):
        revenue = RevenueModel.query.get(rev_id)
        if revenue:
            revenue.name = rev_data["name"]
            revenue.description = rev_data["description"]
            revenue.type = rev_data["type"]
            revenue.amount = rev_data["amount"]
            revenue.category_id = rev_data["category_id"]
        else:
            revenue = RevenueModel(id=rev_id, **rev_data)

        db.session.add(revenue)
        db.session.commit()

        return revenue
    
    def delete(self, rev_id):
        revenue = RevenueModel.query.get_or_404(rev_id)
        raise NotImplementedError("Deleting a revenue is not implemented.")

@blp.route("/revenue")
class RevenueList(MethodView):
    @blp.response(200, RevenueSchema(many=True))
    def get(self):
        return revenues.values()
    
    @blp.arguments(RevenueSchema)
    @blp.response(201, RevenueSchema)
    def post(self, rev_data):
        revenue = RevenueModel(**rev_data)

        try:
            db.session.add(revenue)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error whilst inserting revenue into database")

        return revenue