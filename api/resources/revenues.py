import uuid, datetime
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import revenues
from schemas import RevenueSchema, RevenueUpdateSchema

blp = Blueprint("revenues", __name__, description="Operations on revenues")

@blp.route("/revenue/<string:rev_id>")
class Revenue(MethodView):
    def get(self, rev_id):
        try:
            return revenues[rev_id], 200
        except KeyError:
            abort(404, message="Revenue not found")
    
    @blp.arguments(RevenueUpdateSchema)
    def put(self, rev_data, rev_id):
        try:
            revenue = revenues[rev_id]
            revenue |= rev_data
            return {"message": "Revenue updated"}
        except KeyError:
            abort(404, message="Revenue not found")
    
    def delete(self, rev_id):
        try:
            del revenues[rev_id]
            return {"message": "Revenue deleted"}
        except KeyError:
            abort(404, message="Revenue not found")

@blp.route("/revenue")
class RevenueList(MethodView):
    def get(self):
        return {"revenues": list(revenues.items())}
    
    @blp.arguments(RevenueSchema)
    def post(self, rev_data):
        # TODO: validation that the information is as expected
        rev_id = uuid.uuid4().hex
        rev_created = datetime.datetime.now()
        revenue = {**rev_data, "id": rev_id, "created": rev_created}
        revenues[rev_id] = revenue

        return revenue, 201