from ibc.session import InteractiveBrokersSession


class Alerts():

    def __init__(self, ib_client: object, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `Alerts` client.

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

    def available_alerts(self, account_id: str) -> list:
        """Returns Applicant Id with all owner related entities.

        ### Parameters
        ----
        account_id : str
            The account ID you want a list of alerts for.

        ### Returns
        ----
        list:
            A collection of `Alert` resources.

        ### Usage
        ----
            >>> alerts_service = ibc_client.alerts
            >>> alerts_service.available_alerts(
                account_id=ibc_client.account_number
            )
        """

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/iserver/account/{account_id}/alerts'
        )

        return content

    def mta_alerts(self) -> list:
        """Returns the Mobile Trading Assistant Alert.

        ### Overview
        ----
        Each login user only has one mobile trading assistant (MTA)
        alert with it's own unique tool id. The tool id cannot be
        changed. When modified a new order Id is generated. MTA alerts
        can not be created or deleted. If you call delete 
        /iserver/account/:accountId/alert/:alertId, it will reset MTA
        to default. See here for more information on MTA alerts.

        ### Returns
        ----
        list:
            A collection of `MobileTradingAssistantAlert` resource.

        ### Usage
        ----
            >>> alerts_service = ibc_client.alerts
            >>> alerts_service.mta_alerts()
        """

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/iserver/account/mta'
        )

        return content