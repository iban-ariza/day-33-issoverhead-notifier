"""
Run independently: python -m unittest test_iss.py

Test functions to test API calls and functionality.
"""
import unittest
import requests
from unittest.mock import patch
from app import is_iss_overhead


class TestMain(unittest.TestCase):

    MY_LAT = 51.507351
    MY_LONG = -0.127758

    def test_something(self):
        self.assertNotEqual(True, False)  # add assertion here

    @patch('app.requests.get')     # replaces requests.get in the main module with a mock
    def test_is_iss_directly_overhead(self, mock_get):
        """
        Because there is a raise_for_status within the method, you have
        to make sure that it is also mocked.
        :param mock_get:
        :return:
        """
        mock_get.return_value.json.return_value = {
            "iss_position": {"latitude": self.MY_LAT, "longitude": self.MY_LONG},
            "message": "success",
            "timestamp": 1713808502
        }

        mock_get.return_value.raise_for_status = lambda: None
        self.assertTrue(is_iss_overhead())

    # patch - used to replace function with mock/dummy
    @patch('app.requests.get')
    def test_iss_not_overhead(self, mock_get):
        # Mock response when ISS is not overhead (by 10 error)
        mock_get.return_value.json.return_value = {
            "iss_position": {"latitude": self.MY_LAT + 10, "longitude": self.MY_LONG + 10},
            "message": "success",
            "timestamp": 1713808502
        }
        mock_get.return_value.raise_for_status = lambda: None

        self.assertFalse(is_iss_overhead())

    @patch('app.requests.get')
    def test_api_failure(self, mock_get):
        # Simulate an API failure
        mock_get.side_effect = requests.exceptions.HTTPError("API error")

        with self.assertRaises(requests.exceptions.HTTPError):
            is_iss_overhead()


if __name__ == '__main__':
    unittest.main()
