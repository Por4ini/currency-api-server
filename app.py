import datetime
from flask_smorest import Blueprint
from flask_smorest import Api
from modules.rate import *
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from sqlalchemy import inspect
from flask_apispec.extension import FlaskApiSpec
from modules.schemas import ItemsSchema
from flask_apispec import marshal_with

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://<USERNAME>:<PASSWORD>@<HOST:PORT>/<NAME_DATABASE>"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
date = datetime.date.today()

bp = Blueprint('items', 'items', url_prefix='/api/')

docs = FlaskApiSpec()
docs.init_app(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config.update(
    {
        'APISPEC_SPEC': APISpec(
            title='exchange_rate',
            version='v1',
            openapi_version='2.0',
            plugins=[MarshmallowPlugin()],
        )
    }
)

app.config['API_TITLE'] = 'exchange_rate'
app.config['API_VERSION'] = '1.0'
app.config['OPENAPI_VERSION'] = '2.0'
api = Api(app)

with app.app_context():
    inspector = inspect(db.engine)


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    valid_currencies = ["PLN", "UAH", "EUR", "CAD"]

    try:
        if currency_code in valid_currencies:
            existing_item = Items.query.filter_by(
                currency_code=currency_code, date=str(date.today())
            ).first()
            if existing_item is not None:
                # Update value if item exists
                existing_item.value = get_external_rate(currency_code)
                db.session.commit()
            else:
                # Create new item if it doesn't exist
                new_item = Items(
                    currency_code=currency_code,
                    value=get_external_rate(currency_code),
                    date=date.today(),
                )
                if not inspector.has_table('items'):
                    Items.__table__.create(bind=db.engine)
                db.session.add(new_item)
                db.session.commit()
                db.session.close()

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


@app.route("/api/add", methods=["POST"])
@marshal_with(ItemsSchema(many=True))
def post_rate():
    data = request.get_json()  # Отримуємо дані з запиту в форматі JSON
    currency_code = data.get('currency_code')
    value = get_external_rate(currency_code)
    if not inspector.has_table('items'):
        Items.__table__.create(bind=db.engine)
    existing_item = Items.query.filter_by(
        currency_code=currency_code, date=str(date.today())
    ).first()
    if existing_item is not None:
        return jsonify({'message': 'Item already exists'})
    new_item = Items(
        currency_code=currency_code,
        value=value,
        date=date,
    )

    db.session.add(new_item)
    db.session.commit()
    db.session.close()
    return jsonify({'message': 'New item is created!'})


api.register_blueprint(bp)
docs.register(get_exchange_rate_filter)
docs.register(get_exchange_rate)
docs.register(get_exchange_rate_db)
docs.register(post_rate)

if __name__ == "__main__":
    app.run(debug=False)
