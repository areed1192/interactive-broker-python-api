from ibc.session import InteractiveBrokersSession


class Trades():

    def __init__(self, ib_client: object, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `Trades` client.

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

    def get_trades(self) -> list:
        """Returns a list of trades for the currently selected
        account for current day and six previous days.

        ### Returns
        ----
        list:
            A collection of `Trade` resources.

        ### Usage
        ----
            >>> trades_service = ibc_client.trades
            >>> trades_service.get_trades()
        """

        content = self.session.make_request(
            method='get',
            endpoint='/api/iserver/account/trades'
        )

        return content
