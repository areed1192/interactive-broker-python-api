from ibc.session import InteractiveBrokersSession


class Customer():

    def __init__(self, ib_client: object, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `InteractiveBrokersCustomer` client.

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

    def customer_info(self) -> dict:
        """Returns Applicant Id with all owner related entities.

        ### Returns
        ----
        dict:
            A customer resource object.

        ### Usage
        ----
            >>> customers_service = ibc_client.customers
            >>> customers_service.customer_info()
        """

        content = self.session.make_request(
            method='get',
            endpoint='/api/ibcust/entity/info'
        )

        return content
