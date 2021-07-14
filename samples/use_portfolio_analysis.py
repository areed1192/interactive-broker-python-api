from pprint import pprint
from configparser import ConfigParser
from ibc.client import InteractiveBrokersClient
from ibc.utils.enums import Frequency

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

# Grab the `PortfolioAnalysis` Service.
ib_portfolio_analysis = ibc_client.portfolio_analysis

# Grab our account summary.
pprint(
    ib_portfolio_analysis.account_summary(
        account_ids=[ibc_client.account_number]
    )
)

# Grab the account performance.
pprint(
    ib_portfolio_analysis.account_performance(
        account_ids=[ibc_client.account_number],
        frequency=Frequency.Quarterly
    )
)

# Grab the account performance.
pprint(
    ib_portfolio_analysis.transactions_history(
        account_ids=[ibc_client.account_number]
    )
)
