"""
    ==============================
    Data Store Library API
    ==============================
"""
__version__ = "0.1.0"

import os
import ast
from flask_migrate import Migrate
from flask import request, jsonify, Response, Flask
from flask_json import FlaskJSON, JsonError
from flask_login import LoginManager, login_required

from orm.orm_service import User, db, ORMService
from db.db_service import get_database_uri
from data.data_service import DataService


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
app.secret_key = "Data Storage Library"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
m = Migrate()
m.init_app(app, db, directory=os.path.join("orm", "migrations"))
with app.app_context():
    db.create_all()
login_manager = LoginManager()
login_manager.init_app(app)
ORMService.get_instance().insert_initial_data()


@app.get("/")
def index():
    """Root directory for health check."""
    return jsonify("Data Store Library"), 200


@login_manager.request_loader
def load_user_from_request(request):
    """Load a user with an api key for authentication."""

    req = request.args
    if req:
        api_key = request.args["api_key"]
        if api_key:
            if api_key:
                user = User.query.filter_by(api_key=api_key).first()
                if user:
                    return user
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Unauthorized access."""
    return "Unauthorized access is not possible.", 400


@app.get("/put")
@login_required
def put():
    """Insert one or batch records."""
    req = request.args
    if req is not None:
        records = req["records"]
        files = req["files"]
        destinations = req["destinations"]
        records = ast.literal_eval(records)
        files = ast.literal_eval(files)
        destinations = ast.literal_eval(destinations)
        if records and files and destinations:
            try:
                DataService.get_instance().put(records, files, destinations)
                return jsonify("The data is stored successfully."), 200
            except Exception as e:
                return JsonError(
                    warning=f"There is an error. The reason is {e}.",
                    code=500,
                )
    return JsonError(warning="The syntax of JSON is not suitable", code=400)


@app.get("/update")
@login_required
def update():
    """Update one or batch records."""
    req = request.args
    if req is not None:
        records = req["records"]
        records = ast.literal_eval(records)
        if records:
            try:
                DataService.get_instance().update(records)
                return jsonify("The data is successfully updated."), 200
            except Exception as e:
                return JsonError(
                    warning=f"There is an error. The reason is {e}.",
                    code=500,
                )
    return JsonError(warning="The syntax of JSON is not suitable", code=400)


@app.get("/delete")
@login_required
def delete():
    """delete one or batch records."""
    req = request.args
    if req is not None:
        record_keys = req["record_keys"]
        record_keys = ast.literal_eval(record_keys)
        if record_keys:
            try:
                DataService.get_instance().delete(record_keys)
                return jsonify("The keys are successfully deleted."), 200
            except Exception as e:
                return JsonError(
                    warning=f"There is an error. The reason is {e}.",
                    code=500,
                )
    return JsonError(warning="The syntax of JSON is not suitable", code=400)


@app.get("/filter_records")
@login_required
def filter_records():
    """Filter records."""
    req = request.args
    if req is not None:
        value = limit = offset = None
        if "value" in req:
            value = req["value"]
        if "limit" in req:
            limit = req["limit"]
        if "offset" in req:
            offset = req["offset"]
        if value:
            try:
                data = DataService.get_instance().filter_records(value, limit, offset)
                return jsonify(data), 200
            except Exception as e:
                return JsonError(
                    warning=f"There is an error. The reason is {e}.",
                    code=500,
                )
    return JsonError(warning="The syntax of JSON is not suitable", code=400)


if __name__ == "__main__":
    app.run(debug=True)
