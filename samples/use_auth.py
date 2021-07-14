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

# Grab the `Authentication` Service.
auth_service = ibc_client.authentication

# Login
auth_service.login()

# Wait for the user to login.
while not auth_service.authenticated:
    auth_service.check_auth()

# check if we are authenticated.
pprint(
    auth_service.is_authenticated()
)

# Validate the current session.
pprint(
    auth_service.sso_validate()
)

# Reauthenticate the session.
pprint(
    auth_service.reauthenticate()
)

# Set the account for the server.
pprint(
    auth_service.update_server_account(
        account_id=ibc_client.account_number
    )
)
