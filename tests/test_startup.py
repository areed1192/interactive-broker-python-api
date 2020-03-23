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

# WIDGETS - NEWS BRIEFING
# https://cdcdyn.interactivebrokers.com/portal.proxy/v1/portal/iserver/news/briefing
# https://cdcdyn.interactivebrokers.com/portal.proxy/v1/portal/iserver/news/sources
# https://cdcdyn.interactivebrokers.com/portal.proxy/v1/portal/iserver/news/top
# https://cdcdyn.interactivebrokers.com/portal.proxy/v1/portal/iserver/news/portfolio
# https://cdcdyn.interactivebrokers.com/portal.proxy/v1/portal/metrics/report
# https://cdcdyn.interactivebrokers.com/portal.proxy/v1/mkt/hmds/scanner


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
# https://localhost:5000/v1/portal/fundamentals/landing/265598?widgets=profile,ratings,financials,key_ratios,analyst_forecast,ownership,dividends,competitors,esg,events

# RATION DETAILS
# https://localhost:5000/v1/portal/fundamentals/ratio_details/265598?search_id=C|PENORM,LAST_DAY,0
# https://localhost:5000/v1/portal/fundamentals/ratio_details/265598?search_id=C|PR2TANBK,LAST_DAY,0,((C|TANBVPS,LFI,0))
# https://localhost:5000/v1/portal/fundamentals/ratio_details/265598?search_id=C|GROSMGN,TTM,0



# https://localhost:5000/v1/portal/iserver/marketdata/snapshot?conids=265598&since=0&fields=31,6509,6070,7512,7296

# https://widgets.tipranks.com/api/IB/analystratings?ticker=AAPL
# https://widgets.tipranks.com/api/IB/news?ticker=AAPL
# https://widgets.tipranks.com/api/IB/prices?ticker=AAPL
# https://widgets.tipranks.com/api/IB/hedgefunds?ticker=AAPL

# https://localhost:5000/v1/portal/fundamentals/analyst_forecasts/265598?annual=false&all=true
# https://localhost:5000/v1/portal/fundamentals/dividends/265598
# https://localhost:5000/v1/portal/fundamentals/esg/265598
# https://localhost:5000/v1/portal/fundamentals/persist/search/265598

# https://localhost:5000/v1/portal/calendar/events/
# {"calendar_request":{"date":{"start":"20200208-0800","end":"20200508-0700"},"filters":{"symbol":"10753238","recently_held":"false","corporate_earnings":"true","DivExDates":"true","ipo":"true","splits":"true","corporate_events":"true","economic_events":"false","option_show_monthly":"true","option_show_weekly":"false","country":"All","limit":"250","limit_region":"50"},"account":""}}


# https://localhost:5000/v1/portal/fundamentals/landing/10753238?
# widgets=objective,
# mstar,
# lipper_ratings,
# mf_key_ratios,
# risk_and_statistics,
# holdings,
# performance_and_peers,
# keyProfile,
# ownership,3
# dividends,
# tear_sheet,
# mf_esg

# https://localhost:5000/v1/portal/fundamentals/mf_profile_and_fees/10753238
# https://localhost:5000/v1/portal/fundamentals/mf_lip_ratings/10753238
# https://localhost:5000/v1/portal/fundamentals/mf_performance/10753238?risk_period=6M&statistic_period=6M
# https://localhost:5000/v1/portal/fundamentals/mf_performance_chart/10753238?chart_period=3M
# https://localhost:5000/v1/portal/fundamentals/mf_holdings/10753238
# https://localhost:5000/v1/portal/fundamentals/mf_ratios_fundamentals/10753238
# https://localhost:5000/v1/portal/fundamentals/mf_risks_stats/10753238?period=1Y
# https://localhost:5000/v1/portal/fundamentals/mf_esg/10753238
# https://localhost:5000/v1/portal/fundamentals/ownership/10753238
# https://localhost:5000/v1/portal/fundamentals/dividends/10753238
# https://localhost:5000/v1/portal/fundamentals/research/altavista/10753238
# https://localhost:5000/v1/portal/iserver/marketdata/history?conid=265598&period=2h&bar=1min
# https://localhost:5000/v1/portal/iserver/marketdata/history?conid=265598&period=2h&bar=1min
# https://localhost:5000/v1/portal/iserver/secdef/strikes?conid=265598&sectype=OPT&month=MAR20&exchange=SMART
# https://localhost:5000/v1/portal/iserver/secdef/info?conid=265598&sectype=OPT&month=MAR20&exchange=SMART&strike=297.5&right=P
# https://localhost:5000/v1/portal/iserver/secdef/info?conid=265598&sectype=OPT&month=MAR20&exchange=SMART&strike=297.5&right=C
# https://localhost:5000/v1/portal/iserver/secdef/info?symbol=CL&issuerId=e1377044&sectype=BOND&filters=0:SMART,27:202109
# https://localhost:5000/v1/portal/iserver/marketdata/history?conid=111710390&period=1m&source=m&bar=4h

# 6M
# 1Y
# 3Y
# 5Y
# 10Y
