import json
import re
from collections import Counter
from datetime import datetime

from src.read_from_csv import read_transactions_from_csv
from src.read_from_excel import read_transactions_from_excel


def search_transactions(transactions, search_string):
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    filtered_transactions = [
        transaction for transaction in transactions if pattern.search(transaction.get("description", ""))
    ]
    return filtered_transactions


def count_transactions_by_category(transactions, categories):
    category_counts = Counter()
    for transaction in transactions:
        if transaction["description"] in categories:
            category_counts[transaction["description"]] += 1
    return dict(category_counts)


def load_transactions_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def sort_by_date(filtered_transactions, order="по возрастанию"):
    def date_parser(date_str):
        if "Z" in date_str:
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        else:
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")

    if order == "по возрастанию":
        return sorted(filtered_transactions, key=lambda x: date_parser(x["date"]))
    elif order == "по убыванию":
        return sorted(filtered_transactions, key=lambda x: date_parser(x["date"]), reverse=True)
    else:
        raise ValueError("Invalid order. Please specify 'asc' or 'desc'.")


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input("Пользователь: ")
        if choice in ["1", "2", "3"]:
            break
        else:
            print("Программа: Неправильный ввод. Пожалуйста, выберите пункт от 1 до 3.")

    if choice == "1":
        file_path = input("Введите путь к JSON-файлу: ")
        transactions = load_transactions_from_json(file_path)
        print("Программа: Для обработки выбран JSON-файл.")

    elif choice == "2":
        file_path = input("Введите путь к CSV-файлу: ")
        data = read_transactions_from_csv(file_path)
        print("Программа: Для обработки выбран CSV-файл.")
        transactions = []

        for item in data:
            values = list(item.values())[0].split(";")
            transactions.append(
                {
                    "id": values[0],
                    "state": values[1],
                    "date": values[2],
                    "amount": values[3],
                    "currency_name": values[4],
                    "currency_code": values[5],
                    "from": values[6],
                    "to": values[7],
                    "description": ";".join(values[8:]),
                }
            )
        print("Программа: Для обработки выбран CSV-файл.")

    elif choice == "3":
        file_path = input("Введите путь к XLSX-файлу: ")
        transactions = read_transactions_from_excel(file_path)
        print("Программа: Для обработки выбран XLSX-файл.")

    while True:
        status = input(
            "Введите статус, по которому необходимо выполнить фильтрацию. "
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\nПользователь: "
        ).upper()
        if status in ["EXECUTED", "CANCELED", "PENDING"]:
            break
        else:
            print("Программа: Неправильный ввод. Пожалуйста, выберите один из доступных статусов.")

    filtered_transactions = [t for t in transactions if t.get("state") == status]

    print(f'Программа: Операции отфильтрованы по статусу "{status}"')

    if not filtered_transactions:
        print("Программа: Не найдено ни одной транзакции.")
        return

    while True:
        sort_choice = input("Отсортировать операции по дате? Да/Нет\nПользователь: ").strip().lower()
        if sort_choice in ["да", "нет"]:
            break
        else:
            print("Программа: Неправильный ввод. Пожалуйста, выберите 'Да' или 'Нет'.")

    if sort_choice == "да":
        while True:
            order_choice = input("Отсортировать по возрастанию или по убыванию?\nПользователь: ").strip().lower()
            if order_choice in ["по возрастанию", "по убыванию"]:
                break
            else:
                print("Программа: Неправильный ввод. Пожалуйста, выберите 'по возрастанию' или 'по убыванию'.")
            sort_by_date(filtered_transactions, order_choice)

    while True:
        currency_choice = input("Выводить только рублевые транзакции? Да/Нет\nПользователь: ").strip().lower()
        if currency_choice in ["да", "нет"]:
            break
        else:
            print("Программа: Неправильный ввод. Пожалуйста, выберите 'Да' или 'Нет'.")

    if currency_choice == "да":
        filtered_transactions = [t for t in filtered_transactions if "RUB" in t.get("currency_code", "")]
        print(filtered_transactions)

    while True:
        description_filter = (
            input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\nПользователь: ")
            .strip()
            .lower()
        )
        if description_filter in ["да", "нет"]:
            break
        else:
            print("Программа: Неправильный ввод. Пожалуйста, выберите 'Да' или 'Нет'.")

    if description_filter == "да":
        search_string = input("Введите строку для поиска:")
        filtered_transactions = search_transactions(filtered_transactions, search_string)

        # Выводим результаты
    print("Программа: Распечатываю итоговый список транзакций...")
    if not filtered_transactions:
        print("Программа: Не найдено ни одной транзакции.")
        return

    print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")
    for transaction in filtered_transactions:
        if transaction["description"] == "Открытие вклада":
            print(f"{transaction['date']} {transaction['description']}")
            print(transaction["to"])
            print(f"Сумма: {transaction['amount']} {transaction['currency_code']}\n")
        else:
            print(f"{transaction['date']} {transaction['description']}")
            print(f"{transaction['from']} -> {transaction['to']}")
            print(f"Сумма: {transaction['amount']} {transaction['currency_code']}\n")


if __name__ == "__main__":
    main()
