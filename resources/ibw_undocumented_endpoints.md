# Interactive Brokers Undocumented Endpoints

## News Data

<https://cdcdyn.interactivebrokers.com/portal.proxy/v1/portal/iserver/news/briefing>
<https://cdcdyn.interactivebrokers.com/portal.proxy/v1/portal/iserver/news/sources>
<https://cdcdyn.interactivebrokers.com/portal.proxy/v1/portal/iserver/news/top>
<https://cdcdyn.interactivebrokers.com/portal.proxy/v1/portal/iserver/news/portfolio>
<https://localhost:5000/v1/portal/fundamentals/landing/265598?widgets=news&lang=en>

## Ratios

<https://localhost:5000/v1/portal/fundamentals/ratio_details/265598?search_id=C|PENORM,LAST_DAY,0>
<https://localhost:5000/v1/portal/fundamentals/ratio_details/265598?search_id=C|PR2TANBK,LAST_DAY,0,((C|TANBVPS,LFI,0))>
<https://localhost:5000/v1/portal/fundamentals/ratio_details/265598?search_id=C|GROSMGN,TTM,0>

## Tip Ranks

<https://widgets.tipranks.com/api/IB/analystratings?ticker=AAPL>
<https://widgets.tipranks.com/api/IB/news?ticker=AAPL>
<https://widgets.tipranks.com/api/IB/prices?ticker=AAPL>

## Analyst Forecast

<https://localhost:5000/v1/portal/fundamentals/analyst_forecasts/265598?annual=false&all=true>

## Persist

<https://localhost:5000/v1/portal/fundamentals/persist/search/265598>

## Fundamentals Data

<https://localhost:5000/v1/portal/fundamentals/mf_lip_ratings/10753238>
<https://localhost:5000/v1/portal/fundamentals/mf_performance_chart/10753238?chart_period=3M>
<https://localhost:5000/v1/portal/fundamentals/mf_holdings/10753238>
<https://localhost:5000/v1/portal/fundamentals/mf_ratios_fundamentals/10753238>
<https://localhost:5000/v1/portal/fundamentals/mf_risks_stats/10753238?period=1Y>
<https://localhost:5000/v1/portal/fundamentals/mf_esg/10753238>
<https://localhost:5000/v1/portal/fundamentals/ownership/10753238>
<https://localhost:5000/v1/portal/fundamentals/dividends/10753238>
<https://localhost:5000/v1/portal/fundamentals/research/altavista/10753238>
<https://localhost:5000/v1/portal/fundamentals/landing/10753238>

## Metrics Reporting

<https://cdcdyn.interactivebrokers.com/portal.proxy/v1/portal/metrics/report>

## Scanners

<https://cdcdyn.interactivebrokers.com/portal.proxy/v1/mkt/hmds/scanner>

## 1-Minute Historical Data

<https://localhost:5000/v1/portal/iserver/marketdata/history?conid=265598&period=2h&bar=1min>
<https://localhost:5000/v1/portal/iserver/marketdata/history?conid=111710390&period=1m&source=m&bar=4h>

## Options Contracts - Info

<https://localhost:5000/v1/portal/iserver/secdef/info?conid=265598&sectype=OPT&month=MAR20&exchange=SMART&strike=297.5&right=P>
<https://localhost:5000/v1/portal/iserver/secdef/info?conid=265598&sectype=OPT&month=MAR20&exchange=SMART&strike=297.5&right=C>

## Options Contracts - Strikes

<https://localhost:5000/v1/portal/iserver/secdef/strikes?conid=265598&sectype=OPT&month=MAR20&exchange=SMART>

## Bonds - Info

<https://localhost:5000/v1/portal/iserver/secdef/info?symbol=CL&issuerId=e1377044&sectype=BOND&filters=0:SMART,27:202109>

## Params

```json
{
  "news": {
    "title": "News",
    "content": []
  },
  "top10": {},
  "tear_sheet": {},
  "cumulative_performace": {},
  "objective": {},
  "key_profile": {},
  "ownership": {},
  "risk_statistics": {},
  "dividends": {},
  "overall_ratings": {},
  "mf_esg": {},
  "mf_key_ratios": {}
}
```
