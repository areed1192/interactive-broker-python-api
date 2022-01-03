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

# Grab the `Pnl` Service.
pnl_service = ibc_client.pnl

# Grab the Pnl for the selected server account.
pprint(
    pnl_service.pnl_server_account()
)
