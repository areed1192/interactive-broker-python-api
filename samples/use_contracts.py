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

# Grab the `Contracts` Service.
contracts_service = ibc_client.contracts

# Grab the info for a specific contract.
pprint(
    contracts_service.contract_info(
        contract_id='265598'
    )
)

# Search for Futures Contracts.
pprint(
    contracts_service.search_futures(
        symbols=['CL', 'ES']
    )
)

# Search for multiple contracts.
pprint(
    contracts_service.search_multiple_contracts(
        contract_ids=[265598]
    )
)

# Search for a company by it's ticker.
pprint(
    contracts_service.search_symbol(
        symbol='MSFT',
        name=False
    )
)

# Search for a company by it's name.
pprint(
    contracts_service.search_symbol(
        symbol='Microsoft',
        name=True
    )
)
