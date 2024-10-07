import csv
import json
import re
from datetime import datetime

import pandas as pd

from src.read_from_csv import read_transactions_from_csv
from src.read_from_excel import read_transactions_from_excel


def search_transactions(transactions, search_string):
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    filtered_transactions = [
        transaction for transaction in transactions if pattern.search(transaction.get("description", ""))
    ]
    return filtered_transactions


def count_transactions_by_category(transactions, categories):
    category_counts = {category: 0 for category in categories}
    for transaction in transactions:
        description = transaction.get("description")
        if description in category_counts:
            category_counts[description] += 1
    return category_counts


def load_transactions_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ")

    if choice == "1":
        file_path = input("Введите путь к JSON-файлу: ")
        transactions = load_transactions_from_json(file_path)
        print("Программа: Для обработки выбран JSON-файл.")

    elif choice == "2":
        file_path = input("Введите путь к CSV-файлу: ")
        transactions = read_transactions_from_csv(file_path)
        print("Программа: Для обработки выбран CSV-файл.")

    elif choice == "3":
        file_path = input("Введите путь к XLSX-файлу: ")
        transactions = read_transactions_from_excel(file_path)
        print("Программа: Для обработки выбран XLSX-файл.")

    else:
        print("Программа: Неправильный ввод. Пожалуйста, выберите пункт от 1 до 3.")
        return

    status = input(
        "Введите статус, по которому необходимо выполнить фильтрацию. "
        "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\nПользователь: "
    )

    filtered_transactions = [t for t in transactions if t.get("status") == status.upper()]

    print(f'Программа: Операции отфильтрованы по статусу "{status.upper()}"')

    if not filtered_transactions:
        print("Программа: Не найдено ни одной транзакции.")
        return

    sort_choice = input("Отсортировать операции по дате? Да/Нет\nПользователь: ").strip().lower()
    if sort_choice == "да":
        order_choice = input("Отсортировать по возрастанию или по убыванию?\nПользователь: ").strip().lower()
        reverse = True if order_choice == "по убыванию" else False
        filtered_transactions.sort(key=lambda x: datetime.strptime(x["date"], "%d.%m.%Y"), reverse=reverse)

    currency_choice = input("Выводить только рублевые транзакции? Да/Нет\nПользователь: ").strip().lower()
    if currency_choice == "да":
        filtered_transactions = [t for t in filtered_transactions if "руб" in t.get("amount", "")]

    description_filter = (
        input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\nПользователь: ")
        .strip()
        .lower()
    )
    if description_filter == "да":
        search_string = input("Введите строку для поиска: ")
        filtered_transactions = filter_transactions(filtered_transactions, search_string)

    # Выводим результаты
    print("Программа: Распечатываю итоговый список транзакций...")
    if not filtered_transactions:
        print("Программа: Не найдено ни одной транзакции.")
        return

    print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")
    for transaction in filtered_transactions:
        print(f"{transaction['date']} {transaction['description']}")
        print(f"Счет **{transaction['account']}")
        print(f"Сумма: {transaction['amount']}\n")


if __name__ == "__main__":
    main()
