import requests
from ibw.client import IBClient
from ibw.configAlex import REGULAR_ACCOUNT, REGULAR_PASSWORD, REGULAR_USERNAME, PAPER_ACCOUNT, PAPER_PASSWORD, PAPER_USERNAME

# Create a new session of the IB Web API.
ib_client = IBClient(username=PAPER_USERNAME, password=PAPER_PASSWORD, account=PAPER_ACCOUNT)

# create a new session.
ib_client.create_session()


# https://cdcdyn.interactivebrokers.com/AccountManagement/AmAuthentication?&action=CS_WEB_TICKET&loginType=1#
# https://localhost:5000/AccountManagement/AmAuthentication?&action=CS_WEB_TICKET&loginType=1#

# https://localhost:5000/sso/Login?forwardTo=22&RL=1&ip2loc=off
# https://cdcdyn.interactivebrokers.com/portal/?action=22&RL=1&ip2loc=off


# FUNDAMENTAL DATA - WORKS
# https://localhost:5000/v1/portal/iserver/fundamentals/265598/summary

# NEWS DATA - WORKS
# https://localhost:5000/v1/portal/fundamentals/landing/265598?widgets=news&lang=en

# FINANANCIAL STATEMENTS
# https://localhost:5000/v1/portal/fundamentals/financials/265598?annual=false&type=income
# https://localhost:5000/v1/portal/fundamentals/financials/265598?annual=false&type=income
# https://localhost:5000/v1/portal/fundamentals/financials/265598?annual=false&type=balance
# https://localhost:5000/v1/portal/fundamentals/financials/265598?annual=true&type=balance
# https://localhost:5000/v1/portal/fundamentals/financials/265598?annual=true&type=cash


# MARKET DATA 2 HOUR - 1 MINUTE BAR
# https://localhost:5000/v1/portal/iserver/marketdata/history?conid=265598&period=2h&bar=1min

# PROFILE RATINGS AND MUCH MORE
# https://localhost:5000/v1/portal/fundamentals/landing/265598?widgets=profile,ratings,financials,key_ratios,analyst_forecast,ownership,dividends,competitors,esg,events

# RATION DETAILS
# https://localhost:5000/v1/portal/fundamentals/ratio_details/265598?search_id=C|PENORM,LAST_DAY,0
# https://localhost:5000/v1/portal/fundamentals/ratio_details/265598?search_id=C|PR2TANBK,LAST_DAY,0,((C|TANBVPS,LFI,0))
# https://localhost:5000/v1/portal/fundamentals/ratio_details/265598?search_id=C|GROSMGN,TTM,0



# https://localhost:5000/v1/portal/iserver/marketdata/snapshot?conids=265598&since=0&fields=31,6509,6070,7512,7296

# https://widgets.tipranks.com/api/IB/analystratings?ticker=AAPL
# https://widgets.tipranks.com/api/IB/news?ticker=AAPL
# https://widgets.tipranks.com/api/IB/prices?ticker=AAPL


# https://localhost:5000/v1/portal/fundamentals/analyst_forecasts/265598?annual=false&all=true
# https://localhost:5000/v1/portal/fundamentals/dividends/265598
# https://localhost:5000/v1/portal/fundamentals/esg/265598
# https://localhost:5000/v1/portal/fundamentals/persist/search/265598
