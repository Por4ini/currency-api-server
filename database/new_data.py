from app import *
from my_def.get_data import *

date = datetime.date.today()

list = ['PLN', 'EUR', 'UAH', 'CAD']
def test_connection():
    with app.app_context():
        for item in list:
            new_item = Items(currency_code=item, value=get_external_rate(item), date=date.strftime("%Y-%m-%d"))
            db.session.add(new_item)
            db.session.commit()

test_connection()