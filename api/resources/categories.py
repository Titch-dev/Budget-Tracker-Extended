import uuid, datetime
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import CategoryModel
from schemas import CategorySchema, CategoryUpdateSchema

blp = Blueprint("categories", __name__, description="Operations on categories")

@blp.route("/category/<string:cat_id>")
class Category(MethodView):
    @blp.response(200, CategorySchema)
    def get(self, cat_id):
        category = CategoryModel.query.get_or_404(cat_id)
        return category
    
    @blp.arguments(CategoryUpdateSchema)
    @blp.response(201, CategorySchema)
    def put(self, cat_data, cat_id):
        category = CategoryModel.query.get(cat_id)

        if category:
            category.name = cat_data["name"]
            category.description = cat_data["description"]
            category.budget = cat_data["budget"]
        else:
            category = CategoryModel(id=cat_id, **cat_data)

        db.session.add(category)
        db.session.commit()

        return category
    
    def delete(self, cat_id):
        category = CategoryModel.query.get_or_404(cat_id)
        db.session.delete(category)
        db.session.commit()
        return {"message": "Category successfully deleted"}



@blp.route("/category")
class CategoryList(MethodView):
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        return CategoryModel.query.all()
    
    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, cat_data):
        category = CategoryModel(**cat_data)

        try:
            db.session.add(category)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error when inserting category")

        return category