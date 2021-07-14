from typing import Union
from typing import List
from enum import Enum
from ibc.session import InteractiveBrokersSession


class PortfolioAccounts():

    def __init__(self, ib_client: object, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `PortfolioAccounts` client.

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

    def accounts(self) -> list:
        """Returns the portfolio accounts

        ### Overview
        ----
        In non-tiered account structures, returns a list of accounts
        for which the user can view position and account information.
        This endpoint must be called prior to calling other /portfolio
        endpoints for those accounts. For querying a list of accounts
        which the user can trade, see /iserver/accounts. For a list
        of subaccounts in tiered account structures (e.g. financial 
        advisor or ibroker accounts) see /portfolio/subaccounts.

        ### Returns
        ----
        list: 
            A collection of `PortfolioAccount` resources.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.accounts()
        """

        content = self.session.make_request(
            method='get',
            endpoint='/api/portfolio/accounts'
        )

        self._has_portfolio_been_called = True

        return content

    def subaccounts(self) -> list:
        """Returns the portfolio subaccounts

        ### Overview
        ----
        Used in tiered account structures (such as financial advisor
        and ibroker accounts) to return a list of sub-accounts for
        which the user can view position and account-related information.
        This endpoint must be called prior to calling other /portfolio
        endpoints for those subaccounts. To query a list of accounts
        the user can trade, see /iserver/accounts.

        ### Returns
        ----
        list: 
            A collection of `PortfolioSubAccount` resources.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.subaccounts()
        """

        content = self.session.make_request(
            method='get',
            endpoint='/api/portfolio/subaccounts'
        )

        self._has_sub_portfolio_been_called = True

        return content

    def account_metadata(self, account_id: str) -> dict:
        """Account information related to account Id.

        ### Overview
        --- 
        /portfolio/accounts or /portfolio/subaccounts
        must be called prior to this endpoint.

        ### Returns
        ----
        dict: 
            A `AccountInfo` resource.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.account_metadata(
                account_id=ibc_client.account_number
            )
        """

        if not self._has_portfolio_been_called:
            self.accounts()

        if not self._has_sub_portfolio_been_called:
            self.subaccounts()

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/portfolio/{account_id}/meta'
        )

        return content

    def account_summary(self, account_id: str) -> dict:
        """Returns information about margin, cash balances 
        and other information related to specified account.

        ### Overview
        ----
        `/portfolio/accounts` or `/portfolio/subaccounts`
        must be called prior to this endpoint.

        ### Returns
        ----
        dict: 
            A `AccountSummary` resource.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.account_summary(
                account_id=ibc_client.account_number
            )
        """

        if not self._has_portfolio_been_called:
            self.accounts()

        if not self._has_sub_portfolio_been_called:
            self.subaccounts()

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/portfolio/{account_id}/summary'
        )

        return content

    def account_ledger(self, account_id: str) -> dict:
        """Information regarding settled cash, cash balances,
        etc. in the account’s base currency and any other cash
        balances hold in other currencies.

        ### Overview
        --- 
        `/portfolio/accounts` or `/portfolio/subaccounts`
        must be called prior to this endpoint. The list of 
        supported currencies is available at:
        https://www.interactivebrokers.com/en/index.php?f=3185

        ### Returns
        ----
        dict: 
            A `AccountLedger` resource.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.account_ledger(
                account_id=ibc_client.account_number
            )
        """

        if not self._has_portfolio_been_called:
            self.accounts()

        if not self._has_sub_portfolio_been_called:
            self.subaccounts()

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/portfolio/{account_id}/ledger'
        )

        return content

    def account_allocation(self, account_id: str) -> dict:
        """Information about the account’s portfolio 
        by Asset Class, Industry and Category.

        ### Overview
        --- 
        /portfolio/accounts or /portfolio/subaccounts
        must be called prior to this endpoint. The list of 
        supported currencies is available at:
        https://www.interactivebrokers.com/en/index.php?f=3185

        ### Returns
        ----
        dict: 
            A `AccountAllocation` resource.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.account_allocation(
                account_id=ibc_client.account_number
            )
        """

        if not self._has_portfolio_been_called:
            self.accounts()

        if not self._has_sub_portfolio_been_called:
            self.subaccounts()

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/portfolio/{account_id}/allocation'
        )

        return content

    def portfolio_allocation(self, account_ids: List[str]) -> dict:
        """Similar to /portfolio/{accountId}/allocation but
        returns a consolidated view of of all the accounts
        returned by /portfolio/accounts

        ### Overview
        --- 
        /portfolio/accounts or /portfolio/subaccounts
        must be called prior to this endpoint.

        ### Parameters
        ----
        account_ids : List[str]
            A list of accounts that you want to be consolidated
            into the view.

        ### Returns
        ----
        dict: 
            A consolidated `AccountAllocation` resource.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.portfolio_allocation(
                account_ids=[ibc_client.account_number]
            )
        """

        if not self._has_portfolio_been_called:
            self.accounts()

        if not self._has_sub_portfolio_been_called:
            self.subaccounts()

        payload = {
            'acctIds': account_ids
        }

        content = self.session.make_request(
            method='post',
            endpoint=f'/api/portfolio/allocation',
            json_payload=payload
        )

        return content

    def portfolio_positions(
        self,
        account_id: str,
        page_id: int = 0,
        sort: Union[str, Enum] = None,
        direction: Union[str, Enum] = None,
        period: str = None
    ) -> dict:
        """Returns a list of positions for the given account.
        The endpoint supports paging, page’s default size is
        30 positions.

        ### Overview
        --- 
        /portfolio/accounts or /portfolio/subaccounts
        must be called prior to this endpoint.

        ### Parameters
        ----
        account_id : str
            The account you want to query for positions.

        page_id : int (optional, Default=0)
            The page you want to query.

        sort : Union[str, Enum] (optional, Default=None)
            The field on which to sort the data on.

        direction : Union[str, Enum] (optional, Default=None)
            The order of the sort, `a` means ascending and
            `d` means descending

        period : str (optional, Default=None)
            The period for pnl column, can be 1D, 7D, 1M...

        ### Returns
        ----
        dict: 
            A collection of `PortfolioPosition` resources.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.portfolio_positions(
                    account_id=ibc_client.account_number,
                    page_id=0,
                    sort=SortFields.BaseUnrealizedPnl,
                    direction=SortDirection.Descending
                )
        """

        if not self._has_portfolio_been_called:
            self.accounts()

        if not self._has_sub_portfolio_been_called:
            self.subaccounts()

        if isinstance(sort, Enum):
            sort = sort.value

        if isinstance(direction, Enum):
            direction = direction.value

        params = {
            'sort': sort,
            'direction': direction,
            'period': period
        }

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/portfolio/{account_id}/positions/{page_id}',
            params=params
        )

        return content

    def position_by_contract_id(
        self,
        account_id: str,
        contract_id: str
    ) -> dict:
        """Returns a list of all positions matching the conid. For portfolio models the
        conid could be in more than one model, returning an array with the name of 
        model it belongs to.

        ### Overview
        --- 
        /portfolio/accounts or /portfolio/subaccounts
        must be called prior to this endpoint.

        ### Parameters
        ----
        account_id : str
            The account you want to query for positions.

        contract_id : str
            The contract ID you want to query.

        ### Returns
        ----
        dict: 
            A collection of `PortfolioPosition` resources.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.position_by_contract_id(
                account_id=ibc_client.account_number,
                contract_id='251962528'
            )
        """

        if not self._has_portfolio_been_called:
            self.accounts()

        if not self._has_sub_portfolio_been_called:
            self.subaccounts()

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/portfolio/{account_id}/position/{contract_id}'
        )

        return content

    def positions_by_contract_id(
        self,
        contract_id: str
    ) -> dict:
        """Returns an object of all positions matching the conid for all
        the selected accounts. For portfolio models the conid could be in
        more than one model, returning an array with the name of the model
        it belongs to.

        ### Overview
        --- 
        /portfolio/accounts or /portfolio/subaccounts
        must be called prior to this endpoint.

        ### Parameters
        ----
        contract_id : str
            The contract ID you want to query.

        ### Returns
        ----
        dict: 
            A collection of `PortfolioPosition` resources.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.positions_by_contract_id(
                contract_id='251962528'
            )
        """

        if not self._has_portfolio_been_called:
            self.accounts()

        if not self._has_sub_portfolio_been_called:
            self.subaccounts()

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/portfolio/positions/{contract_id}'
        )

        return content

    def invalidate_positions_cache(
        self,
        account_id: str
    ) -> Union[dict, None]:
        """Invalidates the backend cache of the Portfolio.

        ### Parameters
        ----
        account_id : str
            The account you want to query for positions.

        ### Returns
        ----
        Union[dict, None]: 
            Nothing is returned if successful.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.invalidate_positions_cache()
        """

        content = self.session.make_request(
            method='post',
            endpoint=f'/api/portfolio/{account_id}/positions/invalidate'
        )

        return content
