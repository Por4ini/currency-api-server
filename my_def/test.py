import requests


headers = {
    'accept': 'application/json'
             }
data = {  'currency_code': 1,
    'value' : 2,
    'date' : 3}

url = 'http://127.0.0.1:5000/items'
print(requests.post(url, data=data, headers=headers).text)