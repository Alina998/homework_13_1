import os

import requests
from dotenv import load_dotenv

load_dotenv()  # Загрузка переменных окружения из файла .env

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data"


def convert_to_rubble(transaction):
    currency = transaction["operationAmount"]["currency"]["code"]
    amount = float(transaction["operationAmount"]["amount"])

    # Если валюта уже рубли, просто возвращаем сумму
    if currency == "RUB":
        return amount

    # Если валюта USD или EUR, нужно конвертировать
    if currency in ["USD", "EUR"]:
        url = f"{BASE_URL}/convert?from={currency}&to=RUB&amount={amount}&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            return data["result"]
        else:
            raise Exception(f"Error fetching conversion rate: {data['error']['info']}")

    raise ValueError(f"Unsupported currency: {currency}")
