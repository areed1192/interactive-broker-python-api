from pprint import pprint
from ibw.client import IBClient

# Create a new session of the IB Web API.
ib_client = IBClient(
    username="PAPER_USERNAME",
    account="PAPER_ACCOUNT_ACCOUNT_NUMBER",
    is_server_running=True
)

# create a new session
ib_client.create_session()

# grab the account data.
account_data = ib_client.portfolio_accounts()
pprint(account_data)
pprint('')

# grab account portfolios
account_positions = ib_client.portfolio_account_positions(
    account_id="PAPER_ACCOUNT_ACCOUNT_NUMBER",
    page_id=0
)

pprint(account_positions)
pprint('')

# grab account PNL
account_pnl = ib_client.server_account_pnl()
pprint(account_pnl)
pprint('')

# grab server accounts
server_accounts = ib_client.server_accounts()
pprint(server_accounts)
pprint('')

# Grab historical prices.
aapl_prices = ib_client.market_data_history(
    conid=['265598'],
    period='1d',
    bar='5min'
)
pprint(aapl_prices)
pprint('')

# Grab current quotes
quote_fields = [55, 7296, 7295, 86, 70, 71, 84, 31]
aapl_current_prices = ib_client.market_data(
    conids=['265598'],
    since='0',
    fields=quote_fields
)
pprint(aapl_current_prices)
pprint('')

# search for a symbol
search_symbol_result = ib_client.symbol_search(symbol='AAPL')
pprint(search_symbol_result)
pprint('')

# grab live orders
account_live_orders = ib_client.get_live_orders()
pprint(account_live_orders)
pprint('')

# grab trades
account_trades = ib_client.trades()
pprint(account_trades)
pprint('')

# Do a Futures Search
futures_search = ib_client.futures_search(symbols=['ES'])
pprint(futures_search)
pprint('')

# Grab Portfolio Accounts
portfolio_accounts = ib_client.portfolio_accounts()
pprint(portfolio_accounts)
pprint('')

# Grab Account Info
portfolio_account_info = ib_client.portfolio_account_info(
    account_id="PAPER_ACCOUNT_ACCOUNT_NUMBER"
)
pprint(portfolio_account_info)
pprint('')

# Grab the Positions in the portfolio.
portfolio_positions = ib_client.portfolio_account_positions(
    account_id="PAPER_ACCOUNT_ACCOUNT_NUMBER",
    page_id=0
)
pprint(portfolio_positions)
pprint('')

# Grab the Specific Postion in a Portfolio.
portfolio_position = ib_client.portfolio_account_position(
    account_id="PAPER_ACCOUNT_ACCOUNT_NUMBER",
    conid=272093
)
pprint(portfolio_position)
pprint('')

# Grab a Summary of the Portfolio.
portfolio_summary = ib_client.portfolio_account_summary(
    account_id="PAPER_ACCOUNT_ACCOUNT_NUMBER"
)
pprint(portfolio_summary)
pprint('')

# Grab the Portfolio Ledger.
portfolio_ledger = ib_client.portfolio_account_ledger(
    account_id="PAPER_ACCOUNT_ACCOUNT_NUMBER"
)
pprint(portfolio_ledger)
pprint('')

# Grab the portfolio Allocation.
portfolio_allocation = ib_client.portfolio_account_allocation(
    account_id="PAPER_ACCOUNT_ACCOUNT_NUMBER"
)
pprint(portfolio_allocation)
pprint('')

# Grab Portfolio Allocations.
portfolio_allocations = ib_client.portfolio_accounts_allocation(
    account_ids="PAPER_ACCOUNT_ACCOUNT_NUMBER"
)
pprint(portfolio_allocations)
pprint('')

# Grab Customer Info.
customer_info = ib_client.customer_info()
pprint(customer_info)
pprint('')

# Get the number of Unread messages.
unread_messages = ib_client.get_unread_messages()
unread_for_bn = unread_messages['BN']
pprint(unread_messages)
pprint('')

# Grab the Subscriptions Codes.
subscriptions = ib_client.get_subscriptions()
pprint(subscriptions)
pprint('')

# Grab the Delivery Options for a Subscription.
subscriptions_delivery = ib_client.subscriptions_delivery_options()
pprint(subscriptions_delivery)
pprint('')

# Grab a Discaimer for a specific Subscription.
sub_code = 'M8'
subscriptions_disclaimer = ib_client.subscriptions_disclaimer(
    type_code=sub_code
)
pprint(subscriptions_disclaimer)
pprint('')

# Define a Mutual Fund Contract ID.
mutual_fund_conid = '10753238'

# Grab Fees and Objectives.
mutual_fund_fees = ib_client.mutual_funds_portfolios_and_fees(
    conid=mutual_fund_conid
)
pprint(mutual_fund_fees)
pprint('')

# Possible Values for Performance.
POSSIBLE_VALUES = ['6M', '1Y', '3Y', '5Y', '10Y']

# Grab Performance.
mutual_fund_ratings = ib_client.mutual_funds_performance(
    conid=mutual_fund_conid,
    risk_period='6M',
    yield_period='6M',
    statistic_period='6M'
)
pprint(mutual_fund_ratings)
pprint('')
