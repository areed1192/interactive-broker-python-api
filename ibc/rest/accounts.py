from typing import Union
from typing import List
from enum import Enum
from ibc.session import InteractiveBrokersSession


class Accounts():

    def __init__(self, ib_client: object, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `Accounts` client.

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

    def accounts(self) -> dict:
        """Returns the Users Accounts.

        ### Overview
        ----
        Returns a list of accounts the user has trading access to,
        their respective aliases and the currently selected account.
        Note this endpoint must be called before modifying an order
        or querying open orders.

        ### Returns
        ----
        dict: 
            A collection of `Account` resources.
        """

        content = self.session.make_request(
            method='get',
            endpoint='/api/iserver/accounts'
        )

        return content

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

    def portfolio_accounts(self) -> list:
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
        """

        content = self.session.make_request(
            method='get',
            endpoint='/api/portfolio/accounts'
        )

        self._has_portfolio_been_called = True

        return content

    def portfolio_subaccounts(self) -> list:
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
        """

        if not self._has_portfolio_been_called:
            self.portfolio_accounts()

        if not self._has_sub_portfolio_been_called:
            self.portfolio_subaccounts()

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/portfolio/{account_id}/meta'
        )

        return content

    def account_summary(self, account_id: str) -> dict:
        """Returns information about margin, cash balances 
        and other information related to specified account.

        ### Overview
        --- 
        /portfolio/accounts or /portfolio/subaccounts
        must be called prior to this endpoint.

        ### Returns
        ----
        dict: 
            A `AccountSummary` resource.
        """

        if not self._has_portfolio_been_called:
            self.portfolio_accounts()

        if not self._has_sub_portfolio_been_called:
            self.portfolio_subaccounts()

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
        /portfolio/accounts or /portfolio/subaccounts
        must be called prior to this endpoint. The list of 
        supported currencies is available at:
        https://www.interactivebrokers.com/en/index.php?f=3185

        ### Returns
        ----
        dict: 
            A `AccountLedger` resource.
        """

        if not self._has_portfolio_been_called:
            self.portfolio_accounts()

        if not self._has_sub_portfolio_been_called:
            self.portfolio_subaccounts()

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/portfolio/{account_id}/ledger'
        )

        return content