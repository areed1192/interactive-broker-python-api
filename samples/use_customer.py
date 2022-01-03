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

# Login to a new session.
ibc_client.authentication.login()

# Grab the `Customer` Service.
ib_customer_service = ibc_client.customers

# Grab customer entity info.
pprint(
    ib_customer_service.customer_info()
)
