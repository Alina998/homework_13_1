import unittest
from unittest.mock import Mock, patch

from src.external_api import convert_to_rubble


class TestConvertToRubble(unittest.TestCase):

    @patch("src.external_api.requests.get")
    def test_convert_usd_to_ruble(self, mock_get):
        transaction = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}

        # Настройка mock-ответа от внешнего API
        mock_response = Mock()
        mock_response.json.return_value = {"result": 7000}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = convert_to_rubble(transaction)
        self.assertEqual(result, 7000)
        mock_get.assert_called_once()

    @patch("src.external_api.requests.get")
    def test_convert_eur_to_ruble(self, mock_get):
        transaction = {"operationAmount": {"amount": "100", "currency": {"code": "EUR"}}}

        # Настройка mock-ответа от внешнего API
        mock_response = Mock()
        mock_response.json.return_value = {"result": 8000}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = convert_to_rubble(transaction)
        self.assertEqual(result, 8000)
        mock_get.assert_called_once()

    def test_convert_ruble(self):
        transaction = {"operationAmount": {"amount": "100", "currency": {"code": "RUB"}}}

        result = convert_to_rubble(transaction)
        self.assertEqual(result, 100)

    def test_unsupported_currency(self):
        transaction = {"operationAmount": {"amount": "100", "currency": {"code": "JPY"}}}
        with self.assertRaises(ValueError):
            convert_to_rubble(transaction)


if __name__ == "__main__":
    unittest.main()
