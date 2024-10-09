import json
from io import StringIO
import unittest
from unittest.mock import mock_open, patch

from src.main import count_transactions_by_category, load_transactions_from_json, search_transactions, sort_by_date, filter_transactions_by_status


class TestTransactionFunctions(unittest.TestCase):

    def setUp(self):
        self.transactions = [
            {'id': '2741426', 'state': 'EXECUTED', 'date': '2021-06-25T05:46:42Z', 'amount': '20848', 'currency_name': 'Euro', 'currency_code': 'EUR',
             'from': 'Visa 0928754152447555', 'to': 'American Express 7859387308732251', 'description': 'Перевод с карты на карту'},

            {'id': '1262968', 'state': 'CANCELED', 'date': '2020-03-17T04:51:14Z', 'amount': '14676', 'currency_name': 'Ruble', 'currency_code': 'RUB',
             'from': '', 'to': 'Счет 01445438824868374536', 'description': 'Открытие вклада'},

            {'id': '5080347', 'state': 'PENDING', 'date': '2023-01-28T07:44:09Z', 'amount': '21741', 'currency_name': 'Yuan Renminbi', 'currency_code': 'CNY',
             'from': 'Discover 3148657422735848', 'to': 'Visa 3531923246621737', 'description': 'Перевод с карты на карту'},

            {'id': '2750091', 'state': 'EXECUTED', 'date': '2021-03-15T09:04:23Z', 'amount': '23953', 'currency_name': 'Ruble', 'currency_code': 'RUB',
             'from': 'Mastercard 9726214609905094', 'to': 'American Express 9117693244477013', 'description': 'Перевод с карты на карту'},

            {'id': '4713899', 'state': 'CANCELED', 'date': '2022-10-29T04:47:55Z', 'amount': '24299', 'currency_name': 'Ruble', 'currency_code': 'RUB',
             'from': 'Discover 0096291091971012', 'to': 'Mastercard 3918422798407710', 'description': 'Перевод организации'}
        ]

    def test_search_transactions(self):
        result = search_transactions(self.transactions, "перевод")
        self.assertEqual(len(result), 4)  # Ожидаем, что найдется 4 операции с "перевод"

        result = search_transactions(self.transactions, "открытие")
        self.assertEqual(len(result), 1)  # Ожидаем, что найдется 1 операция с "открытие"

        result = search_transactions(self.transactions, "другое")
        self.assertEqual(len(result), 0)  # Ожидаем, что ничего не будет найдено

    def test_count_transactions_by_category(self):
        categories = ["Перевод с карты на карту", "Открытие вклада", "Перевод организации"]
        result = count_transactions_by_category(self.transactions, categories)
        expected_counts = {"Перевод с карты на карту": 3, "Открытие вклада": 1, "Перевод организации": 1}  # Ожидаемые результаты
        self.assertEqual(result, expected_counts)

    @patch("builtins.open", new_callable=mock_open, read_data='[{"description": "Тест", "amount": "100 руб."}]')
    def test_load_transactions_from_json(self, mock_file):
        transactions = load_transactions_from_json("fake_path.json")
        expected_transactions = [{"description": "Тест", "amount": "100 руб."}]
        self.assertEqual(transactions, expected_transactions)

    def test_sort_by_date(self):
        self.transactions = [{'id': 1, 'date': '2023-10-01T12:00:00.000'},
            {'id': 2, 'date': '2023-09-30T12:00:00.000'},
            {'id': 3, 'date': '2023-10-02T12:00:00Z'},
            {'id': 4, 'date': '2023-09-29T12:00:00.000'}]
        sorted_transactions = sort_by_date(self.transactions, order='по возрастанию')
        self.assertEqual(sorted_transactions[0]['id'], 4)
        self.assertEqual(sorted_transactions[1]['id'], 2)
        self.assertEqual(sorted_transactions[2]['id'], 1)
        self.assertEqual(sorted_transactions[3]['id'], 3)


    @patch('builtins.input', side_effect=["executed"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_filter_transactions_by_status(self, mock_stdout, mock_input):
        transactions = [
            {"state": "EXECUTED", "amount": 100},
            {"state": "CANCELED", "amount": 200},
            {"state": "PENDING", "amount": 300},
        ]
        filter_transactions_by_status(transactions, "executed")
        output = mock_stdout.getvalue().strip().split('\n')
        self.assertIn('Программа: Операции отфильтрованы по статусу "EXECUTED"', output)


if __name__ == "__main__":
    unittest.main()
