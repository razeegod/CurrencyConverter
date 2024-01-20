import json
import requests
from config import currency_dict, API_KEY

class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException(f"Невозможно перевести одинаковые валюты {base}")

        try:
            quote_ticker = currency_dict[quote]
        except KeyError as e:
            raise APIException(f"Некорректный ввод валюты!\nПроверьте ввод валюты {quote}")
        try:
            base_ticker = currency_dict[base]
        except KeyError as e:
            raise APIException(f"Некорректный ввод валюты!\nПроверьте ввод валюты {base}")

        try:
            am = float(amount)
        except ValueError as e:
            raise APIException(f"Некорректный ввод валюты!\nПроверьте ввод валюты {base}")

        r = requests.get(f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{currency_dict[base]}/{currency_dict[quote]}')
        result = json.loads(r.content)

        return result['conversion_rate'] * float(amount)