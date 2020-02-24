
import requests
from ibw.client import IBClient
from ibw.configAlex import REGULAR_ACCOUNT, REGULAR_PASSWORD, REGULAR_USERNAME, PAPER_ACCOUNT, PAPER_PASSWORD, PAPER_USERNAME

# Create a new session of the IB Web API.
ib_client = IBClient(username = PAPER_USERNAME, password = PAPER_PASSWORD, account = PAPER_ACCOUNT)

# create a new session.
ib_client.create_session()

