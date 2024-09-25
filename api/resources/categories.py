import uuid, datetime
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import categories
from schemas import CategorySchema, CategoryUpdateSchema

blp = Blueprint("categories", __name__, description="Operations on categories")

@blp.route("/category/<string:cat_id>")
class Category(MethodView):
    @blp.response(200, CategorySchema)
    def get(self, cat_id):
        try:
            return categories[cat_id], 200
        except KeyError:
            abort(404, message="Category not found")
    
    @blp.arguments(CategoryUpdateSchema)
    @blp.response(201, CategorySchema)
    def put(self, cat_data, cat_id):
        try:
            category = categories[cat_id]
            category |= cat_data
            return category
        except KeyError:
            abort(404, message="Category not found")
    
    def delete(self, cat_id):
        try:
            del categories[cat_id]
            return {"message": "Category deleted"}
        except KeyError:
            abort(404, message="Category not found")


@blp.route("/category")
class CategoryList(MethodView):
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        return categories.values()
    
    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, cat_data):
        # TODO: validation that the information is as expected
        for category in categories.values():
            if category["name"] == cat_data["name"]:
                abort(400, message="Category name already exists")
        
        cat_id = uuid.uuid4().hex
        cat_created = datetime.datetime.now()
        category = {**cat_data, "id": cat_id, "created": cat_created}
        categories[cat_id] = category
        return category