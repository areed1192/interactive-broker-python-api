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

# Grab the `Scanners` Service.
scanners_service = ibc_client.scanners

# Grab the different scanners.
pprint(
    scanners_service.scanners()
)

# Define a scanner.
scanner = {
    "instrument": "STK",
    "type": "NOT_YET_TRADED_TODAY",
    "filter": [
        {
            "code": "priceAbove",
            "value": 50
        },
        {
            "code": "priceBelow",
            "value": 70
        },
        {
            "code": "volumeAbove",
            "value": None
        },
        {
            "code": "volumeBelow",
            "value": None
        }
    ],
    "location": "STK.US.MAJOR",
    "size": "25"
}

# Run that scanner.
pprint(
    scanners_service.run_scanner(
        scanner=scanner
    )
)
