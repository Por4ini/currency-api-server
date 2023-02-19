from my_def.get_data import *
from datetime import datetime
from app import *

with app.app_context():
    items = Items.query.all()
    for item in items:
        print(item.id)
        # db.session.delete(item)
        # db.session.commit()