from typing import Union
from typing import List
from enum import Enum
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
        """

        content = self.session.make_request(
            method='post',
            endpoint='/api/iserver/scanner/run',
            json_payload=scanner
        )

        return content
