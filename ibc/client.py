from ibc.utils.gateway import ClientPortalGateway
from ibc.session import InteractiveBrokersSession
from ibc.utils.auth import InteractiveBrokersAuthentication
from ibc.rest.customer import Customer
from ibc.rest.portfolio_analysis import PortfolioAnalysis
from ibc.rest.accounts import Accounts
from ibc.rest.market_data import MarketData
from ibc.rest.pnl import PnL
from ibc.rest.alert import Alerts


class InteractiveBrokersClient():

    def __init__(self, account_number: str, password: str) -> None:
        """Initializes the `InteractiveBrokersClient` object.

        ### Arguments
        ----
        account_number (str):
            The User's account number they wish to use during the
            session. Can be either their paper trading account or
            their regular account.

        password (str):
            The password associated with the account they've chosen.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
        """

        self._account_number = account_number
        self._password = password

        # Initialize the services that need to start up together.
        self._session = InteractiveBrokersSession(ib_client=self)
        self._auth_service = InteractiveBrokersAuthentication(
            ib_client=self,
            ib_session=self._session
        )

        # Client portal stuff.
        self._client_portal = ClientPortalGateway()
        self._client_portal.setup()

    @property
    def account_number(self) -> str:
        """The User's Interactive Brokers Account Number.

        ### Returns
        ----
        str:
            The account number.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.account_number
        """

        return self._account_number

    @property
    def client_portal(self) -> ClientPortalGateway:
        """Initializes the `ClientPortalGateway` object.

        ### Returns
        ----
        ClientPortalGateway:
            The Interactive Brokers Client Portal Gateway, which is used
            to download the required files needed to access the API.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> ibc_client_portal = ibc_client.client_portal
        """

        return self._client_portal

    def session(self) -> InteractiveBrokersSession:
        """Initializes the `InteractiveBrokersSession` object.

        ### Returns
        ----
        InteractiveBrokersSession:
            Handles all the requests made during your session with
            the Interactive Brokers API.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> ibc_session = ibc_client.session
        """

        return self._session

    @property
    def authentication(self) -> InteractiveBrokersAuthentication:
        """Initializes the `InteractiveBrokersAuthentication` object.

        ### Returns
        ----
        InteractiveBrokersAuthentication:
            Handles authenticating the User so that they can make
            requests to the Interactive Brokers API.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> authentication_service = ibc_client.authentication
        """

        return self._auth_service

    @property
    def customers(self) -> Customer:
        """Initializes the `Customer` object.

        ### Returns
        ----
        Customer:
            Used to grab customer information.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> customer_service = ibc_client.customers
        """

        return Customer(ib_client=self, ib_session=self._session)

    @property
    def portfolio_analysis(self) -> PortfolioAnalysis:
        """Initializes the `PortfolioAnalysis` object.

        ### Returns
        ----
        PortfolioAnalysis:
            Used to interact with the Portfolio Analysis
            service.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> portfolio_analysis_service = ibc_client.portfolio_analysis
        """

        return PortfolioAnalysis(ib_client=self, ib_session=self._session)

    @property
    def accounts(self) -> Accounts:
        """Initializes the `Accounts` object.

        ### Returns
        ----
        Accounts:
            Used to interact with the Accounts
            service.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> accounts_services = ibc_client.accounts
        """

        return Accounts(ib_client=self, ib_session=self._session)

    @property
    def market_data(self) -> MarketData:
        """Initializes the `MarketData` object.

        ### Returns
        ----
        MarketData:
            Used to market quotes and historical prices.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> market_data_services = ibc_client.market_data
        """

        return MarketData(ib_client=self, ib_session=self._session)

    @property
    def pnl(self) -> PnL:
        """Initializes the `PnL` object.

        ### Returns
        ----
        PnL:
            Used to grab Account PNL information.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> pnl_services = ibc_client.pnl
        """

        return PnL(ib_client=self, ib_session=self._session)

    @property
    def alerts(self) -> Alerts:
        """Initializes the `Alerts` object.

        ### Returns
        ----
        Alerts:
            Used to grab, update, and delete Alerts
            associated with your account.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> alerts_services = ibc_client.alerts
        """

        return Alerts(ib_client=self, ib_session=self._session)
