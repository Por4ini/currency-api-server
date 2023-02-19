import datetime
from flask_smorest import Blueprint
from flask_smorest import Api
from modules.rate import *
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from modules.schemas import ItemsSchema
from flask_apispec import marshal_with


app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://habrpguser:Asdf1234@localhost:5432/habrdb"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
date = datetime.datetime.now()



bp = Blueprint('items', 'items', url_prefix='/swagger/')

docs = FlaskApiSpec()
docs.init_app(app)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='exchange_rate',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()]
    )})

app.config['API_TITLE'] = 'exchange_rate'
app.config['API_VERSION'] = '1.0'
app.config['OPENAPI_VERSION'] = '2.0'

api = Api(app)


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency_code = db.Column(db.String())
    value = db.Column(db.String())
    date = db.Column(db.String())


@app.route("/api/<currency_code>&<date>", methods=["GET"])
@marshal_with(ItemsSchema(many=True))
def get_exchange_rate_filter(currency_code, date):
    try:
        items = Items.query.filter(
            Items.currency_code == currency_code, Items.date == date
        ).all()
    except Exception as e:
        return {'message': str(e)}, 400
    return items


@app.route("/api/<currency_code>", methods=["GET"])
def get_exchange_rate(currency_code):
    try:
        items = {
            "currency_code": currency_code,
            "value": get_external_rate(currency_code),
        }
    except Exception as e:
        return {'message': str(e)}, 400
    return jsonify(items)



@app.route("/api/all", methods=["GET"])
@marshal_with(ItemsSchema(many=True))
def get_exchange_rate_db():
    try:
        items = Items.query.all()
    except Exception as e:
        return {'message': str(e)}, 400
    return items




api.register_blueprint(bp)
docs.register(get_exchange_rate_filter)
docs.register(get_exchange_rate)
docs.register(get_exchange_rate_db)


if __name__ == "__main__":
    app.run(debug=True)
