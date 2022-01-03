from configparser import ConfigParser
from ibc.client import InteractiveBrokersClient

# Initialize the Parser.
config = ConfigParser()

# Read the file.
config.read('config/config.ini')

# Get the specified credentials.
account_number = config.get('interactive_brokers_paper', 'paper_account')
account_password = config.get('interactive_brokers_paper', 'paper_password')

# Initialize the `InteractiveBrokersClient` object.
ibc_client = InteractiveBrokersClient(
    account_number=account_number,
    password=account_password
)

# Ensure the portal files are set up.
ibc_client.client_portal.setup()

# Log the user in to the Client Portal Gateway.
ibc_client.authentication.login()
