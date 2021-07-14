from ibc.session import InteractiveBrokersSession


class Scanners():

    def __init__(self, ib_client: object, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `Scanners` client.

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

    def scanners(self) -> dict:
        """Returns an object contains four lists contain all parameters
        for scanners.

        ### Returns
        ----
        dict: 
            A collection of `Scanner` resources.

        ### Usage
        ----
            >>> scanners_service = ibc_client.scanners
            >>> scanners_service.scanners()
        """

        content = self.session.make_request(
            method='get',
            endpoint='/api/iserver/scanner/params'
        )

        return content

    def run_scanner(self, scanner: dict) -> dict:
        """Runs scanner to get a list of contracts.

        ### Parameters
        ----
        scanner : dict
            A scanner definition that you want to run.

        ### Returns
        ----
        dict: 
            A collection of `contract` resources.

        ### Usage
        ----
            >>> scanners_service = ibc_client.scanners
            >>> scanners_service.run_scanner(
                scanner={
                    "instrument": "STK",
                    "type": "NOT_YET_TRADED_TODAY",
                    "filter": [
                        {
                            "code": "priceAbove",
                            "value": 50
                        },
                        {
                            "code": "priceBelow",
                            "value": 70
                        },
                        {
                            "code": "volumeAbove",
                            "value": None
                        },
                        {
                            "code": "volumeBelow",
                            "value": None
                        }
                    ],
                    "location": "STK.US.MAJOR",
                    "size": "25"
                }
            )
        """

        content = self.session.make_request(
            method='post',
            endpoint='/api/iserver/scanner/run',
            json_payload=scanner
        )

        return content
