from typing import List
from ibc.session import InteractiveBrokersSession


class Contracts():

    def __init__(self, ib_client: object, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `Contracts` client.

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

    def contract_info(self, contract_id: str) -> dict:
        """Get contract details, you can use this to prefill your
        order before you submit an order.

        ### Parameters
        ----
        contract_id : str
            The contract ID you want details for.

        ### Returns
        ----
        list:
            A `Contract` resource.

        ### Usage
        ----
            >>> contracts_service = ibc_client.contracts
            >>> contracts_service.contract_info(
                contract_id='265598'
            )
        """

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/iserver/contract/{contract_id}/info'
        )

        return content

    def search_futures(self, symbols: List[str]) -> dict:
        """Returns a list of non-expired future contracts
        for given symbol(s).

        ### Parameters
        ----
        symbols : str
            List of case-sensitive symbols separated by comma

        ### Returns
        ----
        list:
            A collection of `Futures` resource.

        ### Usage
        ----
            >>> contracts_service = ibc_client.contracts
            >>> contracts_service.search_futures(
                symbols=['CL', 'ES']
            )
        """

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/trsrv/futures',
            params={
                'symbols': ','.join(symbols)
            }
        )

        return content

    def search_symbol(self, symbol: str, name: str = False, security_type: str = None) -> list:
        """Search by symbol or name.

        ### Parameters
        ----
        symbol : str
            The symbol to be searched.

        name : bool (optional, Default=False)
            Set to `True` if searching by name, `False` if searching
            by symbol.

        security_type : str (optional, default=True)
            The security type of the symbol.

        ### Returns
        ----
        list:
            A collection of `Contract` resources.

        ### Usage
        ----
            >>> contracts_service = ibc_client.contracts
            >>> contracts_service.search_symbol(
                symbol='AAPL',
                name='Apple'
            )
        """

        payload = {
            'symbol': symbol,
            'name': name,
            'secType': security_type
        }

        content = self.session.make_request(
            method='post',
            endpoint=f'/api/iserver/secdef/search',
            json_payload=payload
        )

        return content

    def search_multiple_contracts(self, contract_ids: List[int]) -> list:
        """Returns a list of security definitions for the given conids.

        ### Parameters
        ----
        contract_ids : List[str]
            A list of Contract IDs.

        ### Returns
        ----
        list:
            A collection of `Contract` resources.

        ### Usage
        ----
            >>> contracts_service = ibc_client.contracts
            >>> contracts_service.search_multiple_contracts(
                contract_ids=['265598']
            )
        """

        payload = {
            "conids": contract_ids
        }

        content = self.session.make_request(
            method='post',
            endpoint=f'/api/trsrv/secdef',
            json_payload=payload
        )

        return content
