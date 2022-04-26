import requests
import json
from config import keys

class ConversionException(Exception):
    pass

class MessageConverter:
    @staticmethod
    def converter(currency: str, base: str, amount: str):

        if currency not in keys.keys() or base not in keys.keys():
            raise ConversionException(
                'One of the currencies is faulty - please check the currencies list (/currencies) for reference.')

        try:
            amount_ = float(amount)
        except ValueError:
            raise ConversionException('Faulty amount - please make sure you input a number.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[currency]}&tsyms={keys[base]}')
        result = json.loads(r.content)[keys[base]] * float(amount)

        return result