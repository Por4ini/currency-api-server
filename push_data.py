from app import Items, app, db
from modules.rate import *
from datetime import datetime

date = datetime.today()
list = ["PLN", "EUR", "UAH", "CAD"]


def push_data(item):
    with app.app_context():
        new_item = Items(
            currency_code=item,
            value=get_external_rate(item),
            date=date.strftime("%Y-%m-%d"),
        )
        db.session.add(new_item)
        db.session.commit()


if __name__ == "__main__":
    for item in list:
        push_data(item)
