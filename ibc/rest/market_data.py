from typing import Union
from typing import List
from enum import Enum
from ibc.session import InteractiveBrokersSession


class MarketData():

    def __init__(self, ib_client, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `MarketData` client.

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

        if self.client.accounts._has_portfolio_been_called:
            self._has_servers_been_called = True
        else:
            print("Calling Accounts Endpoint, so we can pull data.")
            self.client.accounts.accounts()

    def snapshot(self, contract_ids: List[str], since: int = None, fields: Union[str, Enum] = None) -> dict:
        """Get Market Data for the given conid(s). 

        ### Overview
        ----
        The end-point will return by default bid, ask,  last, change, change pct, close, 
        listing exchange. The endpoint /iserver/accounts should be called prior to 
        /iserver/marketdata/snapshot. To receive all available fields the /snapshot
        endpoint will need to be called several times.

        ### Parameters
        ----
        contract_ids : List[str]
            A list of contract Ids.

        frequency : Union[str, Enum]
            Frequency of cumulative performance data
            points: 'D'aily, 'M'onthly,'Q'uarterly. Can
            be one of 3 possible values: "D" "M" "Q".

        ### Returns
        ----
            dict: A `MarketSnapshot` resource.

        ### Usage
        ----
            >>> market_data_services = ibc_client.market_data
            >>> market_data_services.snapshot(contract_ids=['265598'])
        """

        new_fields = []

        if fields:
            # Check for Enums.
            for field in fields:

                if isinstance(field, Enum):
                    field = field.value
                new_fields.append(field)

            fields = ','.join(new_fields)
        else:
            fields = None

        # Define the payload.
        params = {
            'conids': ','.join(contract_ids),
            'since': since,
            'fields': fields
        }

        content = self.session.make_request(
            method='get',
            endpoint='/api/iserver/marketdata/snapshot',
            params=params
        )

        return content

    def market_history(
            self,
            contract_id: str,
            period: str, bar: Union[str, Enum] = None,
            exchange: str = None,
            outside_regular_trading_hours: bool = True
        ) -> dict:
        """Get historical market Data for given conid, length of data
        is controlled by 'period' and 'bar'. 

        ### Parameters
        ----
        contract_id : str
            A contract Id.

        period : str
            Available time period: {1-30}min, {1-8}h,
            {1-1000}d, {1-792}w, {1-182}m, {1-15}y

        bar : Union[str, Enum] (optional, Default=None):
            The bar type you want the data in.

        exchange : str (optional, Default=None):
            Exchange of the conid.

        outside_regular_trading_hours : bool (optional, Default=True)
            For contracts that support it, will determine if historical
            data includes outside of regular trading hours.

        ### Returns
        ----
            dict: A collection `Bar` resources.
        
        ### Usage
        ----
            >>> market_data_services = ibc_client.market_data
            >>> market_data_services.snapshot(contract_ids=['265598'])
        """

        if isinstance(bar, Enum):
            bar = bar.value

        payload = {
            'conid': contract_id,
            'period': period,
            'bar': bar,
            'exchange': exchange,
            'outsideRth': outside_regular_trading_hours
        }

        content = self.session.make_request(
            method='get',
            endpoint='/api/iserver/marketdata/history',
            params=payload
        )

        return content
