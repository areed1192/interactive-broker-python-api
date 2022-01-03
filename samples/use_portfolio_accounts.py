from pprint import pprint
from configparser import ConfigParser
from ibc.client import InteractiveBrokersClient
from ibc.utils.enums import SortDirection
from ibc.utils.enums import SortFields

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

# Grab the `PortfolioAccounts` Service.
portfolio_accounts_services = ibc_client.portfolio_accounts

# Grab the Portfolio Accounts.
pprint(
    portfolio_accounts_services.accounts()
)

# Grab the Portfolio SubAccounts.
pprint(
    portfolio_accounts_services.subaccounts()
)

# Grab the Account metadata.
pprint(
    portfolio_accounts_services.account_metadata(account_id=account_number)
)

# Grab the Account Summary.
pprint(
    portfolio_accounts_services.account_summary(account_id=account_number)
)

# Grab the Account Ledger.
pprint(
    portfolio_accounts_services.account_ledger(account_id=account_number)
)

# Grab the Account Allocation.
pprint(
    portfolio_accounts_services.account_allocation(account_id=account_number)
)

# Grab a consolidated view.
pprint(
    portfolio_accounts_services.portfolio_allocation(
        account_ids=[ibc_client.account_number]
    )
)

# Grab postions from our Portfolio.
pprint(
    portfolio_accounts_services.portfolio_positions(
        account_id=ibc_client.account_number,
        page_id=0,
        sort=SortFields.BaseUnrealizedPnl,
        direction=SortDirection.Descending
    )
)

# Grab positions that fall under a certain contract ID, for a specific account.
pprint(
    portfolio_accounts_services.position_by_contract_id(
        account_id=ibc_client.account_number,
        contract_id='251962528'
    )
)

# Grab positions that fall under a certain contract ID, for all accounts.
pprint(
    portfolio_accounts_services.positions_by_contract_id(
        contract_id='251962528'
    )
)

# Invalidate the backend positions cahce.
pprint(
    portfolio_accounts_services.invalidate_positions_cache(
        account_id=ibc_client.account_number
    )
)
