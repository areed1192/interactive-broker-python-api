import unittest

from unittest import TestCase
from configparser import ConfigParser
from ibc.client import InteractiveBrokersClient
from ibc.rest.market_data import MarketData
from ibc.rest.accounts import Accounts
from ibc.rest.portfolio_analysis import PortfolioAnalysis
from ibc.rest.customer import Customer
from ibc.session import InteractiveBrokersSession
from ibc.utils.gateway import ClientPortalGateway


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

    def test_creates_instance_of_client(self):
        """Create an instance and make sure it's a `InteractiveBrokerClient`."""

        self.assertIsInstance(
            self.ibc_client,
            InteractiveBrokersClient
        )

    def test_creates_instance_of_session(self):
        """Create an instance and make sure it's a `InteractiveBrokerSession`."""

        self.assertIsInstance(
            self.ibc_client.session,
            InteractiveBrokersSession
        )

    def test_creates_instance_of_gateway(self):
        """Create an instance and make sure it's a `ClientPortalGateway`."""

        self.assertIsInstance(
            self.ibc_client.client_portal,
            ClientPortalGateway
        )

    def test_creates_instance_of_market_data(self):
        """Create an instance and make sure it's a `MarketData`client."""

        self.assertIsInstance(
            self.ibc_client.market_data,
            MarketData
        )

    def test_creates_instance_of_accounts(self):
        """Create an instance and make sure it's a `Accounts`client."""

        self.assertIsInstance(
            self.ibc_client.accounts,
            Accounts
        )

    def test_creates_instance_of_portfolio_analysis(self):
        """Create an instance and make sure it's a `PortfolioAnalysis`client."""

        self.assertIsInstance(
            self.ibc_client.portfolio_analysis,
            PortfolioAnalysis
        )

    def test_creates_instance_of_customer(self):
        """Create an instance and make sure it's a `Customer`client."""

        self.assertIsInstance(
            self.ibc_client.customers,
            Customer
        )

    def tearDown(self) -> None:
        """Teardown the `InteractiveBroker` Client."""

        del self.ibc_client


if __name__ == '__main__':
    unittest.main()
