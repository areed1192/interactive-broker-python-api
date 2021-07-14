
from pprint import pprint
from configparser import ConfigParser
from ibc.client import InteractiveBrokersClient
from ibc.utils.enums import BarTypes

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

# Grab the `MarketData` Service.
market_data_services = ibc_client.market_data

# Grab a Quote Snapshot.
pprint(
    market_data_services.snapshot(
        contract_ids=['265598']
    )
)

# Grab Market History.
pprint(
    market_data_services.market_history(
        contract_id='265598',
        period='5d',
        bar=BarTypes.FiveMinute
    )
)
