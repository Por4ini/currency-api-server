import datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import request
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from modules.schemas import ItemsSchema
from flask_apispec import use_kwargs, marshal_with

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://habrpguser:Asdf1234@localhost:5432/habrdb"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
date = datetime.datetime.now()

docs = FlaskApiSpec()
docs.init_app(app)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='exchange_rate',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/'
})


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency_code = db.Column(db.String())
    value = db.Column(db.String())
    date = db.Column(db.String())


@app.route('/items/<currency_code>&<date>', methods=['GET'])
@marshal_with(ItemsSchema(many=True))
def get_exchange_rate(currency_code, date):
    if request.method == 'GET':
        items = Items.query.filter(Items.currency_code == currency_code, Items.date == date).all()
        return items


@app.route('/items/all', methods=['GET'])
@marshal_with(ItemsSchema(many=True))
def get_exchange_rate_db():
    if request.method == 'GET':
        items = Items.query.all()
        return items


if __name__ == "__main__":
    app.run(debug=True)
