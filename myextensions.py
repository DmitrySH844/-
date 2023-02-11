import requests
import json
from myconfig import exchanges_ru
from myconfig import exchanges_en

class APIException(Exception):
    pass

class Converter_ru:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges_ru[base]
        except KeyError:
            return APIException(f"Валюта {base} не найдена!")
        try:
            sym_key = exchanges_ru[sym]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')
        
        r = requests.get(f"https://api.exchangerate.host/latest?base={base_key}&symbols={sym_key}")
        resp = json.loads(r.content)
        new_price = resp['rates'][sym_key] * float(amount)
        return round(new_price, 2)

class Converter_en:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges_en[base]
        except KeyError:
            return APIException(f"Currency {base} not found!")
        try:
            sym_key = exchanges_en[sym]
        except KeyError:
            raise APIException(f"Currency {sym} not found!")

        if base_key == sym_key:
            raise APIException(f'Unable to transfer identical currencies {base}!')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')
        
        r = requests.get(f"https://api.exchangerate.host/latest?base={base_key}&symbols={sym_key}")
        resp = json.loads(r.content)
        new_price = resp['rates'][sym_key] * float(amount)
        return round(new_price, 2)
