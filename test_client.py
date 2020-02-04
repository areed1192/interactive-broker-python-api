from ibw.client import IBClient
from ibw.config import REGULAR_ACCOUNT, REGULAR_PASSWORD, REGULAR_USERNAME, PAPER_ACCOUNT, PAPER_PASSWORD, PAPER_USERNAME

# Create a new session of the IB Web API.
ib_session = IBClient(username = REGULAR_USERNAME, password = REGULAR_PASSWORD, account = REGULAR_ACCOUNT)

# Connect to the session.
ib_session.connect()

# Validate the current session
ib_session.validate()

# Grab historical prices.
aapl_prices = ib_session.market_data_history(conid = ['265598'], period = '1d', bar = '5min')

# print the prices.
print(aapl_prices)