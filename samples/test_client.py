import pprint
import pathlib
from configparser import ConfigParser
from ibw.client import IBClient

# Grab configuration values.
config = ConfigParser()
file_path = pathlib.Path(__file__).parent.parent.joinpath('config','config.ini').resolve()
config.read(file_path)

# Load the details.
PAPER_ACCOUNT = config.get('main','PAPER_ACCOUNT')
PAPER_USERNAME = config.get('main','PAPER_USERNAME')

# Create a new session of the IB Web API.
ib_client = IBClient(username=PAPER_USERNAME, account=PAPER_ACCOUNT)

'''
    SESSIONS
'''

# create a new session
ib_client.create_session()

# Logout of the client.
logout_response = ib_client.logout()
print(logout_response)

# close the current session.
ib_client.close_session()


# '''
#     ACCOUNT DETAILS
# '''


# # grab the account data.
# account_data = ib_client.portfolio_accounts()
# print(account_data)
# print('')

# # grab account portfolios
# account_positions = ib_client.portfolio_account_positions(account_id = PAPER_ACCOUNT, page_id = 0)
# print(account_positions)
# print('')

# # grab account PNL
# account_pnl = ib_client.server_account_pnl()
# print(account_pnl)
# print('')

# # grab server accounts
# server_accounts = ib_client.server_accounts()
# print(server_accounts)
# print('')


# '''
#     PRICES
# '''


# # Grab historical prices.
# aapl_prices = ib_client.market_data_history(conid = ['265598'], period = '1d', bar = '5min')
# print(aapl_prices)
# print('')

# # Grab current quotes
# quote_fields = [55, 7296, 7295, 86, 70, 71, 84, 31]
# aapl_current_prices = ib_client.market_data(conids = ['265598'], since = '0', fields = quote_fields)
# print(aapl_current_prices)
# print('')


# '''
#     FUNDAMENTALS
# '''


# # Grab the quarterly income statement
# aapl_income_statement = ib_client.fundamentals_financials(conid = '265598', financial_statement='income', period = 'quarter')
# print(aapl_income_statement)
# print('')

# # Grab the annual income statement
# aapl_balance_sheet = ib_client.fundamentals_financials(conid = '265598', financial_statement='balance', period = 'annual')
# print(aapl_balance_sheet)
# print('')

# # Grab Key Ratios for Apple.
# aapl_key_ratios = ib_client.fundamentals_key_ratios(conid = '265598')
# print(aapl_key_ratios)
# print('')

# # Grab Dividends for Apple.
# aapl_dividends = ib_client.fundamentals_dividends(conid = '265598')
# print(aapl_dividends)
# print('')

# # Grab ESG (Environmental, Social, and Governance) for Apple.
# aapl_esg = ib_client.fundamentals_esg(conid = '265598')
# print(aapl_esg)
# print('')


# '''
#     DATA
# '''


# # search for a symbol
# search_symbol_result = ib_client.symbol_search(symbol = 'AAPL')
# print(search_symbol_result)
# print('')

# # Grab the news
# aapl_news = ib_client.data_news(conid = '265598')
# print(aapl_news)
# print('')

# # Grab the analyst ratings for Apple
# aapl_analyst_ratings = ib_client.data_ratings(conid = '265598')
# print(aapl_analyst_ratings)
# print('')

# # Grab Ownership details for Apple
# aapl_ownership = ib_client.data_ownership(conid = '265598')
# print(aapl_ownership)
# print('')

# # Grab Comeptitor Details For Apple
# aapl_competitors = ib_client.data_competitors(conid = '265598')
# print(aapl_competitors)
# print('')

# # Grab Analyst Forecast for Apple
# aapl_analyst_forecast = ib_client.data_analyst_forecast(conid = '265598')
# print(aapl_analyst_forecast)
# print('')


# '''
#     ORDERS AND TRADES
# '''


# # grab live orders
# account_live_orders = ib_client.get_live_orders()
# print(account_live_orders)
# print('')

# # grab trades
# account_trades = ib_client.trades()
# print(account_trades)
# print('')


'''
    FUTURES SEARCH
'''

# # Do a Futures Search
# futures_search = ib_client.futures_search(symbols = ['ES'])
# pprint.pprint(futures_search)
# print('')

'''
    PORTFOLIO ACCOUNTS
'''

# # Grab Portfolio Accounts
# portfolio_accounts = ib_client.portfolio_accounts()
# pprint.pprint(portfolio_accounts)
# print('')

# # Grab Account Info
# portfolio_account_info = ib_client.portfolio_account_info(account_id=PAPER_ACCOUNT)
# pprint.pprint(portfolio_account_info)
# print('')

# # Grab the Positions in the portfolio.
# portfolio_positions = ib_client.portfolio_account_positions(account_id = PAPER_ACCOUNT, page_id = 0)
# pprint.pprint(portfolio_positions)
# print('')

# # Grab the Specific Postion in a Portfolio.
# portfolio_position = ib_client.portfolio_account_position(account_id=PAPER_ACCOUNT, conid = 272093)
# pprint.pprint(portfolio_position)
# print('')

# # Grab a Summary of the Portfolio.
# portfolio_summary = ib_client.portfolio_account_summary(account_id=PAPER_ACCOUNT)
# pprint.pprint(portfolio_summary)
# print('')

# # Grab the Portfolio Ledger.
# portfolio_ledger = ib_client.portfolio_account_ledger(account_id=PAPER_ACCOUNT)
# pprint.pprint(portfolio_ledger)
# print('')

# # Grab the portfolio Allocation.
# portfolio_allocation = ib_client.portfolio_account_allocation(account_id=PAPER_ACCOUNT)
# pprint.pprint(portfolio_allocation)
# print('')

# # Grab Portfolio Allocations.
# portfolio_allocations = ib_client.portfolio_accounts_allocation(account_ids=PAPER_ACCOUNT)
# pprint.pprint(portfolio_allocations)
# print('')

'''
    CUSTOMER
'''

# # Grab Customer Info.
# customer_info = ib_client.customer_info()
# pprint.pprint(customer_info)
# print('')

# # Get the number of Unread messages.
# unread_messages = ib_client.get_unread_messages()
# unread_for_bn = unread_messages['BN']
# pprint.pprint(unread_messages)
# print('')

# # Grab the Subscriptions Codes.
# subscriptions = ib_client.get_subscriptions()
# pprint.pprint(subscriptions)
# print('')

# # Grab the Delivery Options for a Subscription.
# subscriptions_delivery = ib_client.subscriptions_delivery_options()
# pprint.pprint(subscriptions_delivery)
# print('')

# # Grab a Discaimer for a specific Subscription.
# sub_code = 'M8'
# subscriptions_disclaimer = ib_client.subscriptions_disclaimer(type_code = sub_code)
# pprint.pprint(subscriptions_disclaimer)
# print('')


'''
    MUTUAL FUNDS
'''


# # Define a Mutual Fund Contract ID.
# mutual_fund_conid = '10753238'

# # Grab Fees and Objectives.
# mutual_fund_fees = ib_client.mutual_funds_portfolios_and_fees(conid = mutual_fund_conid)
# pprint.print(mutual_fund_fees)
# print('')

# # Possible Values for Performance.
# POSSIBLE_VALUES = ['6M', '1Y', '3Y', '5Y', '10Y']

# # Grab Performance.
# mutual_fund_ratings = ib_client.mutual_funds_performance(conid = mutual_fund_conid, risk_period = '6M', yield_period= '6M', statistic_period = '6M')
# pprint.print(mutual_fund_ratings)
# print('')