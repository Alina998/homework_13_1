import unittest
from unittest.mock import patch

import pandas as pd

from src.read_from_excel import read_transactions_from_excel


class TestReadTransactionsFromCSV(unittest.TestCase):

    @patch("pandas.read_excel")  # Замена read_excel на mock
    def test_read_transactions_from_excel(self, mock_read_excel):
        # Подготовим тестовые данные в виде DataFrame
        test_data = {
            "operationAmount": [100, 150, 200],
            "currency": ["RUB", "USD", "EUR"],
        }
        mock_read_excel.return_value = pd.DataFrame(test_data)

        file_path = "dummy_path.xlsx"  # Путь к файлу, который не будет использован
        transactions = read_transactions_from_excel(file_path)

        # Ожидаемое значение
        expected_transactions = [
            {"operationAmount": 100, "currency": "RUB"},
            {"operationAmount": 150, "currency": "USD"},
            {"operationAmount": 200, "currency": "EUR"},
        ]

        # Проверяем, что функция возвращает ожидаемые значения
        self.assertEqual(transactions, expected_transactions)
        # Проверяем, что mock был вызван с правильным аргументом
        mock_read_excel.assert_called_once_with(file_path)

    @patch("pandas.read_excel")
    def test_read_transactions_from_excel_error(self, mock_read_excel):
        # На этот раз сделаем так, чтобы чтение Excel файла выдало ошибку
        mock_read_excel.side_effect = Exception("File not found")

        file_path = "dummy_path.xlsx"
        transactions = read_transactions_from_excel(file_path)

        # Ожидаем, что результат будет пустым списком
        self.assertEqual(transactions, [])
        # Убедимся, что mock был вызван
        mock_read_excel.assert_called_once_with(file_path)


if __name__ == "__main__":
    unittest.main()
