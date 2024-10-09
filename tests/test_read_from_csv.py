import unittest
from unittest.mock import patch
import pandas as pd
from io import StringIO
from src.read_from_csv import read_transactions_from_csv


class TestReadTransactionsFromCSV(unittest.TestCase):

    @patch("pandas.read_csv")
    def test_read_transactions_from_csv(self, mock_read_csv):
        # Подготовим наш тестовый CSV в виде строки
        csv_data = """operationAmount,currency
100,RUB
150,USD
200,EUR
"""
        # Создаем DataFrame как будто это считанный CSV
        mock_read_csv.return_value = pd.read_csv(StringIO(csv_data))

        # Путь к файлу, на самом деле он не будет использован из-за mock
        file_path = "fake_path.csv"

        # Вызов тестируемой функции
        transactions = read_transactions_from_csv(file_path)

        # Ожидаемое значение
        expected_transactions = [
            {"operationAmount": "100", "currency": "RUB"},
            {"operationAmount": "150", "currency": "USD"},
            {"operationAmount": "200", "currency": "EUR"},
        ]

        # Проверяем, что функция возвращает ожидаемые значения
        self.assertEqual(transactions, expected_transactions)
        # Убедимся, что mock был вызван с правильным аргументом
        mock_read_csv.assert_called_once_with(file_path)

    @patch("pandas.read_csv")
    def test_read_transactions_from_csv_error(self, mock_read_csv):
        # На этот раз сделаем так, чтобы чтение CSV файла выдало ошибку
        mock_read_csv.side_effect = Exception("File not found")

        file_path = "fake_path.csv"
        transactions = read_transactions_from_csv(file_path)

        # Ожидаем, что результат будет пустым списком
        self.assertEqual(transactions, [])
        # Убедимся, что mock был вызван
        mock_read_csv.assert_called_once_with(file_path)


if __name__ == "__main__":
    unittest.main()
