order = {
    'price':10.00,
    'quantity':200.00,
    'quantityType':'DOLLARS',
    'symbol':'MSFT'
}

payload = {
    "orderType": "LIMIT",
    "price": 30.00,
    "session": "NORMAL",
    "duration": "DAY",
    "orderStrategyType": "SINGLE",
    "orderLegCollection":
    [
        {"instruction": "BUY",
         "quantity": 200.00,
         "quantityType": "DOLLARS",
         "instrument":{
            "symbol": "MSFT",
            "assetType": "EQUITY",
         },
         }
    ],
    "specialInstruction": "ALL_OR_NONE"
}
