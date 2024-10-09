import unittest
from unittest.mock import patch

import pandas as pd

from src.read_from_csv import read_transactions_from_csv


class TestReadTransactionsFromCSV(unittest.TestCase):

    @patch("pandas.read_csv")
    def test_read_transactions_success(self, mock_read_csv):
        # Настройка mock для pd.read_csv
        mock_data = pd.DataFrame({"id": [1, 2], "amount": [100, 200], "date": ["2023-01-01", "2023-01-02"]})
        mock_read_csv.return_value = mock_data

        result = read_transactions_from_csv("fake_path.csv")

        expected = [{"id": 1, "amount": 100, "date": "2023-01-01"}, {"id": 2, "amount": 200, "date": "2023-01-02"}]
        self.assertEqual(result, expected)

    @patch("pandas.read_csv")
    def test_read_transactions_with_empty_file(self, mock_read_csv):
        # Настройка mock для пустого DataFrame
        mock_data = pd.DataFrame(columns=["id", "amount", "date"])
        mock_read_csv.return_value = mock_data

        result = read_transactions_from_csv("fake_path.csv")

        expected = []
        self.assertEqual(result, expected)

    @patch("pandas.read_csv")
    def test_read_transactions_failure(self, mock_read_csv):
        # Настройка mock для генерации исключения
        mock_read_csv.side_effect = Exception("File not found")

        result = read_transactions_from_csv("fake_path.csv")

        expected = []
        self.assertEqual(result, expected)
        # Можно также проверить вывод в консоль, если это требуется


if __name__ == "__main__":
    unittest.main()
