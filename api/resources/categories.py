from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError


from db import db
from models import CategoryModel, AccountModel
from schemas import CategorySchema, CategoryUpdateSchema

blp = Blueprint("categories", __name__, description="Operations on categories")

@blp.route("/category/<int:cat_id>")
class Category(MethodView):
    @jwt_required()
    @blp.response(200, CategorySchema)
    def get(self, cat_id):
        acc_id = get_jwt_identity()
        category = CategoryModel.query.get_or_404(cat_id)
        if not category.account_id == acc_id:
            abort(409, message="Category not belonging to account")
        return category
    
    @jwt_required()
    @blp.arguments(CategoryUpdateSchema)
    @blp.response(200, CategorySchema)
    def put(self, cat_data, cat_id):
        acc_id = get_jwt_identity()
        category = CategoryModel.query.get_or_404(cat_id)
        if not category.account_id == acc_id:
            abort(409, message="Category not belonging to account")
        
        if category:
            # Update only the fields the client has posted
            for key in cat_data.keys():
                if hasattr(category, key):
                    setattr(category, key, cat_data[key])

        db.session.add(category)
        db.session.commit()

        return category
    
    @jwt_required()
    def delete(self, cat_id):
        acc_id = get_jwt_identity()
        category = CategoryModel.query.get_or_404(cat_id)
        if not category.account_id == acc_id:
            abort(409, message="Category not belonging to account")
        db.session.delete(category)
        db.session.commit()
        return {"message": "Category successfully deleted"}



@blp.route("/category")
class CategoryList(MethodView):
    @jwt_required()
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        acc_id = get_jwt_identity()
        return CategoryModel.query.filter(CategoryModel.account_id==acc_id)
    
    @jwt_required()
    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, cat_data):
        # Constraint on if category name exists for account
        acc_id = get_jwt_identity()
        if CategoryModel.query.filter(
                                        CategoryModel.account_id == acc_id,
                                        CategoryModel.name == cat_data["name"]
                                    ).first():
            abort(400, message="Category name already exists")
        
        category = CategoryModel(account_id=acc_id, **cat_data)

        try:
            db.session.add(category)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error when inserting category")

        return category
