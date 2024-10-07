import json
import unittest
from unittest.mock import mock_open, patch

from src.main import count_transactions_by_category, load_transactions_from_json, search_transactions


class TestTransactionFunctions(unittest.TestCase):

    def setUp(self):
        self.transactions = [
            {
                "description": "Перевод",
                "amount": "100 руб.",
                "status": "EXECUTED",
                "date": "10.01.2022",
                "account": "1234",
            },
            {
                "description": "Кредит",
                "amount": "200 USD",
                "status": "EXECUTED",
                "date": "11.01.2022",
                "account": "5678",
            },
            {
                "description": "Депозит",
                "amount": "500 руб.",
                "status": "CANCELED",
                "date": "12.01.2022",
                "account": "9101",
            },
            {
                "description": "Перевод",
                "amount": "150 руб.",
                "status": "PENDING",
                "date": "13.01.2022",
                "account": "1213",
            },
        ]

    def test_search_transactions(self):
        result = search_transactions(self.transactions, "перевод")
        self.assertEqual(len(result), 2)  # Ожидаем, что найдется 2 операции с "перевод"

        result = search_transactions(self.transactions, "кредит")
        self.assertEqual(len(result), 1)  # Ожидаем, что найдется 1 операция с "кредит"

        result = search_transactions(self.transactions, "другое")
        self.assertEqual(len(result), 0)  # Ожидаем, что ничего не будет найдено

    def test_count_transactions_by_category(self):
        categories = ["Перевод", "Кредит", "Депозит"]
        result = count_transactions_by_category(self.transactions, categories)
        expected_counts = {"Перевод": 2, "Кредит": 1, "Депозит": 0}  # Ожидаемые результаты
        self.assertEqual(result, expected_counts)

    @patch("builtins.open", new_callable=mock_open, read_data='[{"description": "Тест", "amount": "100 руб."}]')
    def test_load_transactions_from_json(self, mock_file):
        transactions = load_transactions_from_json("fake_path.json")
        expected_transactions = [{"description": "Тест", "amount": "100 руб."}]
        self.assertEqual(transactions, expected_transactions)


if __name__ == "__main__":
    unittest.main()
