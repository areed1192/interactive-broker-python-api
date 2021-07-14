import unittest

from unittest import TestCase
from configparser import ConfigParser
from ibc.client import InteractiveBrokersClient
from ibc.rest.market_data import MarketData


class InteractiveBrokersClientTest(TestCase):

    """Will perform a unit test for the `InteractiveBrokersClient` session."""

    def setUp(self) -> None:
        """Set up the InteractiveBroker Client."""

        # Initialize the Parser.
        config = ConfigParser()

        # Read the file.
        config.read('config/config.ini')

        # Get the specified credentials.
        account_number = config.get(
            'interactive_brokers_paper', 'paper_account')
        account_password = config.get(
            'interactive_brokers_paper', 'paper_password')

        # Initialize the client.
        self.ibc_client = InteractiveBrokersClient(
            account_number=account_number,
            password=account_password
        )

    def test_creates_instance_of_session(self):
        """Create an instance and make sure it's a `InteractiveBroker`."""

        self.assertIsInstance(
            self.ibc_client,
            InteractiveBrokersClient
        )

    def test_creates_instance_of_marke_data(self):
        """Create an instance and make sure it's a `MarketData`client."""

        self.assertIsInstance(
            self.ibc_client.market_data,
            MarketData
        )

    def tearDown(self) -> None:
        """Teardown the `InteractiveBroker` Client."""

        del self.ibc_client


if __name__ == '__main__':
    unittest.main()
