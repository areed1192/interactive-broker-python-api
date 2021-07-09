
from typing import List
from typing import Dict
from typing import Union
from ibc.utils.gateway import ClientPortalGateway
from ibc.session import InteractiveBrokersSession
from ibc.utils.auth import InteractiveBrokersAuthentication


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
        """

        self._account_number = account_number
        self._password = password

        # Initialize the services that need to start up together.
        self._session = InteractiveBrokersSession(ib_client=self)
        self._auth_service = InteractiveBrokersAuthentication(            
            ib_client=self, 
            ib_session=self._session
        )
        self._client_portal = ClientPortalGateway()

        self._client_portal.setup()

    def __repr__(self):
        pass

    @property
    def account_number(self) -> str:
        """The User's Interactive Brokers Account Number.

        ### Returns
        ----
        str:
            The account number.
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
        """

        return self._client_portal

    def session(self) -> InteractiveBrokersSession:
        """Initializes the `InteractiveBrokersSession` object.

        ### Returns
        ----
        InteractiveBrokersSession:
            Handles all the requests made during your session with
            the Interactive Brokers API.
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
        """

        return self._auth_service
