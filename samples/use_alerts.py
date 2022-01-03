from pprint import pprint
from configparser import ConfigParser
from ibc.client import InteractiveBrokersClient

# Initialize the Parser.
config = ConfigParser()

# Read the file.
config.read('config/config.ini')

# Get the specified credentials.
account_number = config.get('interactive_brokers_paper', 'paper_account')
account_password = config.get('interactive_brokers_paper', 'paper_password')

# Initialize the client.
ibc_client = InteractiveBrokersClient(
    account_number=account_number,
    password=account_password
)

# Initialize the Authentication Service.
auth_service = ibc_client.authentication

# Login
auth_service.login()

# Wait for the user to login.
while not auth_service.authenticated:
    auth_service.check_auth()

# Grab the `Alerts` Service.
alerts_service = ibc_client.alerts

# Grab the Available alerts for our account.
pprint(
    alerts_service.available_alerts(
        account_id=ibc_client.account_number
    )
)

# Grab the MTA Alerts.
pprint(
    alerts_service.mta_alerts()
)
