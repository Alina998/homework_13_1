import pandas as pd

from src.external_api import convert_to_rubble

def read_transactions_from_csv(file_path):
    """Функция считывает данные из CSV файла и возвращает список транзакций"""
    try:
        df = pd.read_csv(file_path)
        transactions = df.to_dict(orient="records")
        return transactions
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return []


if __name__ == "__main__":
    file_path = "C:/Users/pasta/Desktop/homework_13_1/data/transactions.csv"

    # Считываем транзакции из CSV файла
    transactions = read_transactions_from_csv(file_path)

    # Обрабатываем каждую транзакцию
    for transaction in transactions:
        try:
            result = convert_to_rubble(transaction)
            print(f"Transaction: {transaction}, Converted amount in RUB: {result}")
        except Exception as e:
            print(f"Error processing transaction {transaction}: {e}")
