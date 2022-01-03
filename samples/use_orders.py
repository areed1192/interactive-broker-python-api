from email import message
from pprint import pprint
from configparser import ConfigParser

from numpy import isin
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

# Grab the `Orders` Service.
orders_services = ibc_client.orders

# Grab all the orders we have.
pprint(
    orders_services.orders()
)

# Define an order.
order_template = {
    "conid": 251962528,
    "secType": "362673777:STK",
    # Keep in mind that this order ID is valid for 24 hours, can't use it twice.
    "cOID": "limit-buy-order-v1",
    "orderType": "LMT",
    "price": 5.00,
    "side": "BUY",
    "quantity": 1,
    "tif": "DAY"
}


# Place an order, good chance I will get `Reply` back.
order_placement_response = orders_services.place_order(
    account_id=ibc_client.account_number,
    order=order_template
)

pprint(
    order_placement_response
)

if isinstance(order_placement_response, list):
    order_response = order_placement_response[0]

    if 'id' in order_response:
        message_id = order_response['id']

# Reply to the message.
pprint(
    orders_services.reply(
        reply_id=message_id,
        message={
            "confirmed": True
        }
    )
)

bracket_order_template = {
    "orders": [
        {
            "conid": 251962528,
            "secType": "362673777:FUT",
            "cOID": "buy-1",
            "orderType": "LMT",
            "side": "BUY",
            "price": 9.00,
            "quantity": 1,
            "tif": "DAY"
        },
        {
            "conid": 251962528,
            "secType": "362673777:STK",
            # This MUST match the `cOID` of the first order.
            "parentId": "buy-1",
            "orderType": "LMT",
            "side": "BUY",
            "price": 7.00,
            "quantity": 2,
            "tif": "DAY"
        }
    ]
}

# Place a bracket order, good chance I will get `Reply` back.
pprint(
    orders_services.place_bracket_order(
        account_id=ibc_client.account_number,
        orders=bracket_order_template
    )
)

# Delete an order.
pprint(
    orders_services.delete_order(
        account_id=ibc_client.account_number,
        order_id='1915650541'
    )
)

# Modify an order.
modify_order_response = orders_services.modify_order(
    account_id=ibc_client.account_number,
    order_id='1915650539',
    order={
        "conid": 251962528,
        "secType": "362673777:STK",
        "cOID": "limit-buy-order-3",
        "orderType": "LMT",
        "price": 7.00,
        "side": "BUY",
        "quantity": 1,
        "tif": "DAY"
    }
)

# Print the response.
pprint(
    modify_order_response
)

# Place an order, good chance I will get `Reply` back.
pprint(
    orders_services.place_whatif_order(
        account_id=ibc_client.account_number,
        order=order_template
    )
)
