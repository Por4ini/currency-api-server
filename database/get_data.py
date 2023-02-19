from modules.get_data import *
from datetime import datetime
from app import *

with app.app_context():
    items = Items.query.all()
    for item in items:
        print(item.date)
        # db.session.delete(item)
        # db.session.commit()e