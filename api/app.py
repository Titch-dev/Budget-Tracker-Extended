from flask import Flask
from flask_smorest import Api

from resources.accounts import blp as AccountBlueprint
from resources.revenues import blp as RevenueBlueprint
from resources.categories import blp as CategoryBlueprint
from resources.recurrents import blp as RecurrentBlueprint
from resources.goals import blp as GoalsBlueprint


app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True  # extension exceptions will be raised
app.config["API_TITLE"] = "Budget Tracker API"  # smorest - doc title
app.config["API_VERSION"] = "v1"  # smorest - doc api version
app.config["OPENAPI_VERSION"] = "3.0.3"  # smorest to use doc standard 3.0.3
app.config["OPENAPI_URL_PREFIX"] = "/"  # tells smorest what the route of the api is
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"  # smorest uses swagger ui
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(AccountBlueprint)
api.register_blueprint(RevenueBlueprint)
api.register_blueprint(CategoryBlueprint)
api.register_blueprint(RecurrentBlueprint)
api.register_blueprint(GoalsBlueprint)