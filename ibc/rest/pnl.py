from ibc.session import InteractiveBrokersSession


class PnL():

    def __init__(self, ib_client: object, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `PnL` client.

        ### Parameters
        ----
        ib_client : object
            The `InteractiveBrokersClient` Python Client.

        ib_session : InteractiveBrokersSession
            The IB session handler.
        """

        from ibc.client import InteractiveBrokersClient

        self.client: InteractiveBrokersClient = ib_client
        self.session: InteractiveBrokersSession = ib_session
        self._has_portfolio_been_called = False
        self._has_sub_portfolio_been_called = False

    def pnl_server_account(self) -> dict:
        """Returns an object containing PnL for the selected account
        and its models (if any).

        ### Returns
        ----
        dict: 
            An `AccountPnL` resource.
        """

        content = self.session.make_request(
            method='get',
            endpoint='/api/iserver/account/pnl/partitioned'
        )

        return content
