#### Table of Contents

- [Overview](#overview)
- [What's in the API](#whats-in-the-api)
- [Requirements](#requirements)
- [API Key & Credentials](#api-key-and-credentials)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Documentation & Resources](#documentation-and-resources)
- [Support These Projects](#support-these-projects)

## Overview

The unofficial Python API client library for Interactive Broker Client Portal Web API allows individuals with Interactive Broker accounts to manage trades, pull historical and real-time data, manage their accounts, create and modify orders all using the Python programming language.

Interactive Broker offers multiple APIs for their clients. If you would like to learn more about their API offerings click on the links below:

- TradeStation API, please refer to the [official documentation](http://interactivebrokers.github.io/tws-api/)
- Client Portal API, please refer to the [official documentation](https://interactivebrokers.github.io/cpwebapi/)
- Third Party API, plesfe refer to the [official documentation](https://www.interactivebrokers.com/webtradingapi/)

## What's in the API

- Authentication
- Account Endpoints
- Market Data Endpoints
- Trade Endpoints
- Portfolio Endpoints
- Scanner Endpoints
- Portfolio Analysis Endpoints
- Web Streaming

## Requirements

The following requirements must be met to use this API:

- A Interactive Broker account, you'll need your account password and account number to use the API.
- [Java 8](https://developers.redhat.com/products/openjdk/download) update 192 or higher installed (gateway is compatible with higher Java versions including OpenJDK 11).
- Download the [Client Portal Gateway](https://www.interactivebrokers.com/en/index.php?f=45185)

## API Key and Credentials

The API does not require any API keys to use it, all of the authentication is handled by the Client Portal Gateway. Everytime a user starts a new session with the API they will need to proivde their login credentials for the account they wish to use. The Interactive Broker Web API does offer the ability to use the API using a paper account.

**Important:** Your account number and account password should be kept secret.

## Installation

PLACE HOLDER FOR PIP INSTALLATION

## Usage

This example demonstrates how to login to the API and demonstrates sending a request using the `market_data_history` endpoint, using your API key.

```python
from ibw.client import IBClient

REGULAR_ACCOUNT = 'MY_ACCOUNT_NUMBER'
REGULAR_PASSWORD = 'MY_ACCOUNT_PASSWORD'
REGULAR_USERNAME = 'MY_ACCOUNT_USERNAME'

# Create a new session of the IB Web API.
ib_session = IBClient(username = REGULAR_USERNAME, password = REGULAR_PASSWORD, account = REGULAR_ACCOUNT)

# create a new session.
ib_client.create_session()

# grab the account data.
account_data = ib_client.portfolio_accounts()

# print the data.
print(account_data)

# Grab historical prices.
aapl_prices = ib_client.market_data_history(conid = ['265598'], period = '1d', bar = '5min')

# print the prices.
print(aapl_prices)

# close the current session.
ib_client.close_session()
```

## Features

### Request Validation

For certain requests, in a limited fashion, it will help validate your request when possible. For example, when grabbing real-time quotes using the `market_data` endpoint, it will validate the fields you request to ensure they're valid fields for that endpoint.

## Documentation and Resources

### Official API Documentation

- [Getting Started](https://interactivebrokers.github.io/cpwebapi/index.html#login)
- [Endpoints](https://interactivebrokers.com/api/doc.html)
- [Websockets](https://interactivebrokers.github.io/cpwebapi/RealtimeSubscription.html)

## Support these Projects

**Patreon:**
Help support this project and future projects by donating to my [Patreon Page](https://www.patreon.com/sigmacoding). I'm always looking to add more content for individuals like yourself, unfortuantely some of the APIs I would require me to pay monthly fees.

**YouTube:**
If you'd like to watch more of my content, feel free to visit my YouTube channel [Sigma Coding](https://www.youtube.com/c/SigmaCoding).

**Hire Me:**
If you have a project, you think I can help you with feel free to reach out at coding.sigma@gmail.com
