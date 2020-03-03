
import requests
from ibw.client import IBClient
from ibw.configAlex import REGULAR_ACCOUNT, REGULAR_PASSWORD, REGULAR_USERNAME, PAPER_ACCOUNT, PAPER_PASSWORD, PAPER_USERNAME

# # Create a new session of the IB Web API.
# ib_client = IBClient(username=PAPER_USERNAME, password=PAPER_PASSWORD, account=PAPER_ACCOUNT)

# # create a new session.
# ib_client.create_session()

headers = {
    'Host': "cdcdyn.interactivebrokers.com",
    'Cookies':'SBID=vb96cgi81glk780ddeu; web=705854992; _gcl_au=1.1.1284437508.1583006317; _ga=GA1.2.836477598.1583006317; _fbp=fb.1.1583006317086.262525416; IB_SP_TST=www1; sptst=1; rdt_uuid=e3a5565d-3ed8-40be-a295-a0488e11cf69; _ga=GA1.3.836477598.1583006317; RL=1; REGION=cdcdyn; fwdTo=22; ptc=""; IB_LANG=en; pastandalone=""; ibcust=f5f31370-f907-43c3-b86d-3060c7010c8c; IBTOOLS_ACCT_ID=U3367556; ibotcookieinit=true; ibotcookieinitforced=true; PHPSESSID=2b9egno6uhvduausig7d190r57; IB_SEARCH=1583200365; _gid=GA1.2.1507183800.1583200366; _gid=GA1.3.1507183800.1583200366; URL_PARAM="forwardTo=22&RL=1&ip2loc=US"; XYZAB_AM.LOGIN=c2e2197bfa135412e4107dcf5b122caa281ba837; XYZAB=c2e2197bfa135412e4107dcf5b122caa281ba837; USERID=45632284; cp=be261038-c5ae-42d9-9177-ecad3e8c3537'
}

response = requests.get(url = r"https://cdcdyn.interactivebrokers.com/portal.proxy/v1/portal/iserver/fundamentals/265598/summary")
print(response.content)
print(response.cookies.items())

# https://localhost:5000/v1/portal/iserver/fundamentals/265598/summary