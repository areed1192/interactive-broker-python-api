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

# Login first.
ibc_client.authentication.login()

# Grab the `Accounts` Service.
accounts_services = ibc_client.accounts

# Grab the User's Accounts.
pprint(
    accounts_services.accounts()
)

# Grab the Pnl for the Server Portfolio..
pprint(
    accounts_services.pnl_server_account()
)
