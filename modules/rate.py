import requests


def get_external_rate(currency_code):
    url = f"https://v6.exchangerate-api.com/v6/d3a5989ba09e8d982986ee75/latest/{currency_code}"
    result = requests.get(url).json()
    if result["result"] == "success":
        print(
            f'Успішний запит, отримано співвідношення {currency_code} до USD: {result["conversion_rates"]["USD"]}'
        )

        return float(result["conversion_rates"]["USD"])
    else:
        print("Введіть валідне значення валюти")
