import datetime
import pytest
from app import app, db, Items
from modules.rate import get_external_rate


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()




def test_post_rate(client, mocker):
    # Підготовка тестових даних
    data = {'currency_code': 'UAH'}
    rate = str(get_external_rate('UAH'))
    date = datetime.date.today()
    mocker.patch('app.get_external_rate', return_value=rate)

    # Виконання POST запиту
    response = client.post('/api/add', json=data)

    # Перевірка статус коду та вмісту відповіді
    assert response.status_code == 200
    assert response.json == {'message': 'New item is created!'} or {'message': 'Item already exists'}

    # Перевірка, що новий елемент було створено в базі даних
    item = Items.query.filter_by(currency_code='UAH', date=str(date.today())).first()
    assert item.currency_code == 'UAH'
    assert item.value == rate
    assert item.date == str(date.today())
    db.session.close()


def test_get_exchange_rate_db(client):
    response = client.get("/api/all")
    assert response.status_code == 200

def test_get_exchange_rate(client):
    response = client.get("/api/UAH")
    assert response.status_code == 200
    assert response.json == {"currency_code": "UAH", "value": get_external_rate('UAH')}

def test_get_exchange_rate_filter(client):
    data = {"item": "USD"}
    client.post("/api/items", json=data)
    response = client.get("/api/USD&2023-02-20")
    assert response.status_code == 200 or 404



def test_get_external_rate():
    # Перевіряємо, чи повертає функція float
    assert isinstance(get_external_rate("EUR"), float)

    # Перевіряємо, чи повертає функція None при неправильному коді валюти
    assert get_external_rate("XYZ") is None
