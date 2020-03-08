from ibw.client import IBClient
from ibw.configAlex import REGULAR_ACCOUNT, REGULAR_PASSWORD, REGULAR_USERNAME, PAPER_ACCOUNT, PAPER_PASSWORD, PAPER_USERNAME

# Create a new session of the IB Web API.
ib_client = IBClient(username = PAPER_USERNAME, password = PAPER_PASSWORD, account = PAPER_ACCOUNT)


'''
    SESSIONS
'''


# create a new session.
ib_client.create_session()

# close the current session.
# ib_client.close_session()


'''
    ACCOUNT DETAILS
'''


# grab the account data.
account_data = ib_client.portfolio_accounts()
print(account_data)
print('')

# grab account portfolios
account_positions = ib_client.portfolio_account_positions(account_id = PAPER_ACCOUNT, page_id = 0)
print(account_positions)
print('')

# grab account PNL
account_pnl = ib_client.server_account_pnl()
print(account_pnl)
print('')

# grab server accounts
server_accounts = ib_client.server_accounts()
print(server_accounts)
print('')


'''
    PRICES
'''


# Grab historical prices.
aapl_prices = ib_client.market_data_history(conid = ['265598'], period = '1d', bar = '5min')
print(aapl_prices)
print('')

# Grab current quotes
quote_fields = [55, 7296, 7295, 86, 70, 71, 84, 31]
aapl_current_prices = ib_client.market_data(conids = ['265598'], since = '0', fields = quote_fields)
print(aapl_current_prices)
print('')


'''
    FUNDAMENTALS
'''


# Grab the quarterly income statement
aapl_income_statement = ib_client.fundamentals_financials(conid = '265598', financial_statement='income', period = 'quarter')
print(aapl_income_statement)
print('')

# Grab the annual income statement
aapl_balance_sheet = ib_client.fundamentals_financials(conid = '265598', financial_statement='balance', period = 'annual')
print(aapl_balance_sheet)
print('')

# Grab Key Ratios for Apple.
aapl_key_ratios = ib_client.fundamentals_key_ratios(conid = '265598')
print(aapl_key_ratios)
print('')

# Grab Dividends for Apple.
aapl_dividends = ib_client.fundamentals_dividends(conid = '265598')
print(aapl_dividends)
print('')

# Grab ESG (Environmental, Social, and Governance) for Apple.
aapl_esg = ib_client.fundamentals_esg(conid = '265598')
print(aapl_esg)
print('')


'''
    DATA
'''


# search for a symbol
search_symbol_result = ib_client.symbol_search(symbol = 'AAPL')
print(search_symbol_result)
print('')

# Grab the news
aapl_news = ib_client.data_news(conid = '265598')
print(aapl_news)
print('')

# Grab the analyst ratings for Apple
aapl_analyst_ratings = ib_client.data_ratings(conid = '265598')
print(aapl_analyst_ratings)
print('')

# Grab Ownership details for Apple
aapl_ownership = ib_client.data_ownership(conid = '265598')
print(aapl_ownership)
print('')

# Grab Comeptitor Details For Apple
aapl_competitors = ib_client.data_competitors(conid = '265598')
print(aapl_competitors)
print('')

# Grab Analyst Forecast for Apple
aapl_analyst_forecast = ib_client.data_analyst_forecast(conid = '265598')
print(aapl_analyst_forecast)
print('')


'''
    ORDERS AND TRADES
'''


# grab live orders
account_live_orders = ib_client.get_live_orders()
print(account_live_orders)
print('')

# grab trades
account_trades = ib_client.trades()
print(account_trades)
print('')
