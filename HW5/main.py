from typing import Any
import json

with open('chf_rates.json') as json_file:
    CHF_RATE = json.load(json_file)
    CURRENCIES = list(CHF_RATE['forward'].keys())

class Price:
    def __init__(self, value: int, currency: str):
        self.value: int = value
        self.currency: str = currency

    def __str__(self) -> str:
        return f"Price: {self.value} {self.currency}"

    def __add__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise ValueError("Can perform operation only with Pirces objects")
        else:
            if self.currency == other.currency:
                return Price(value=self.value + other.value, currency=self.currency)
            if self.currency in CURRENCIES and other.currency in CURRENCIES:
                return (self.convert(to="CHF") + other.convert(to="CHF")).convert(to=self.currency)
            else:
                raise ValueError("Non-convertable currency")

    def __sub__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise ValueError("Can perform operation only with Pirces objects")
        else:
            if self.currency == other.currency:
                return Price(value=self.value - other.value, currency=self.currency)
            if self.currency in CURRENCIES and other.currency in CURRENCIES:
                return (self.convert(to="CHF") - other.convert(to="CHF")).convert(to=self.currency)

    def convert(self, to: str) -> "Price":
        if to == "CHF":
            value = self.value * CHF_RATE['backward'][self.currency]
            return Price(value=value, currency="CHF")
        if to in CURRENCIES and to != "CHF":
            value = self.value * CHF_RATE['forward'][self.currency]
            return Price(value=value, currency=to)

def main():
    try:
        phone = Price(value=200, currency="USD")
        tablet = Price(value=400, currency="EUR")

        total: Price = phone + tablet
        print(total)

        difference: Price = tablet - phone
        print(difference)
    catch Exception as e:
        print(e)