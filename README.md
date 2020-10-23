# Unofficial Interactive Brokers API

## Table of Contents

- [Overview](#overview)
- [What's in the API](#whats-in-the-api)
- [Setup Requirements](#setup-requirements)
- [Setup Client Portal](#setup-client-portal)
- [Setup API Key & Credentials](#setup-api-key-and-credentials)
- [Setup Installation](#setup-installation)
- [Setup Writing Account Information](#setup-writing-account-information)
- [Usage](#usage)
- [Features](#features)
- [Documentation & Resources](#documentation-and-resources)
- [Support These Projects](#support-these-projects)

## Overview

The unofficial Python API client library for Interactive Broker Client Portal Web API allows individuals with Interactive Broker accounts to manage trades, pull historical and real-time data, manage their accounts, create and modify orders all using the Python programming language.

Interactive Broker offers multiple APIs for their clients. If you would like to learn more about their API offerings click on the links below:

- Trade Workstation API, please refer to the [official documentation](http://interactivebrokers.github.io/tws-api/)
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

## Setup Requirements

The following requirements must be met to use this API:

- A Interactive Broker account, you'll need your account password and account number to use the API.
- [Java 8](https://developers.redhat.com/products/openjdk/download) update 192 or higher installed (gateway is compatible with higher Java versions including OpenJDK 11).
- Download the [Beta Client Portal Gateway](https://www.interactivebrokers.com/en/index.php?f=45185)

## Setup Client Portal

Once you've downloaded the latest client portal or if you chose to use the one provided by the repo. You need to unzip the folder and place it in the repo where this code is stored.

## Setup API Key and Credentials

The API does not require any API keys to use it, all of the authentication is handled by the Client Portal Gateway. Everytime a user starts a new session with the API they will need to proivde their login credentials for the account they wish to use. The Interactive Broker Web API does offer the ability to use the API using a paper account.

**Important:** Your account number and account password should be kept secret.

## Setup Installation

```console
pip install interactive-broker-python-web-api
```

## Setup Writing Account Information

The Client needs specific account information to create a and validate a new session. Where you choose to store this information is up to you, but I'll layout some options here.

**Write a Config File:**

It's common in Python to have a config file that contains information you need to use during the setup of a script. Additionally, you can make this file in a standard way so that way it's easy to read everytime. In Python, there is a module called `configparser` which can be used to create config files that mimic that of Windows INI files.

To create a config file using hte `configparser` module, run the script below in a separate file or go to the [Resources Folder](https://github.com/areed1192/interactive-broker-python-api/tree/master/resources) and run the `write_config.py` file.

```python
import pathlib
from configparser import ConfigParser

# Initialize a new instance of the `ConfigParser` object.
config = ConfigParser()

# Define a new section called `main`.
config.add_section('main')

# Set the values for the `main` section.
config.set('main', 'REGULAR_ACCOUNT', 'YOUR_ACCOUNT_NUMBER')
config.set('main', 'REGULAR_USERNAME', 'YOUR_ACCOUNT_USERNAME')

config.set('main', 'PAPER_ACCOUNT', 'YOUR_ACCOUNT_NUMBER')
config.set('main', 'PAPER_USERNAME', 'YOUR_ACCOUNT_USERNAME')

# Make the `config` folder for the user.
new_directory = pathlib.Path("config/").mkdir(parents=True, exist_ok=True)

# Write the contents of the `ConfigParser` object to the `config.ini` file.
with open('config/config.ini', 'w+') as f:
    config.write(f)
```

**Store the Variables in the Script:**

If you plan to not share the script with anyone else, then you can store the account info inside the script itself. However, please make sure that you do not make the file public to individuals you don't know.

## Usage

This example demonstrates how to login to the API and demonstrates sending a request using the `market_data_history` endpoint, using your API key.

```python
from ibw.client import IBClient

REGULAR_ACCOUNT = 'MY_ACCOUNT_NUMBER'
REGULAR_USERNAME = 'MY_ACCOUNT_USERNAME'

# Create a new session of the IB Web API.
ib_client = IBClient(
    username=REGULAR_USERNAME,
    account=REGULAR_ACCOUNT,
    is_server_running=True
)

# create a new session.
ib_client.create_session()

# grab the account data.
account_data = ib_client.portfolio_accounts()

# print the data.
print(account_data)

# Grab historical prices.
aapl_prices = ib_client.market_data_history(conid=['265598'], period='1d', bar='5min')

# print the prices.
print(aapl_prices)

# close the current session.
ib_client.close_session()
```

## Features

### Request Validation

For certain requests, in a limited fashion, it will help validate your request when possible. For example, when grabbing real-time quotes using the `market_data` endpoint, it will validate the fields you request to ensure they're valid fields for that endpoint.

### Endpoint Verification

To use certain endpoints, you must call other endpoints before you use it. To help limit the amount of confusion for users, the library will call those endpoints for you behind the scenes so that way you don't need to worry about it.

### Client Portal Download

If the user doesn't have the clientportal gateway downloaded, then the library will download a copy it, unzip it for you, and quickly allow you to get up and running with your scripts.

## Documentation and Resources

- [Getting Started](https://interactivebrokers.github.io/cpwebapi/index.html#login)
- [Endpoints](https://interactivebrokers.com/api/doc.html)
- [Websockets](https://interactivebrokers.github.io/cpwebapi/RealtimeSubscription.html)

## Support these Projects

**Patreon:**
Help support this project and future projects by donating to my [Patreon Page](https://www.patreon.com/sigmacoding). I'm always looking to add more content for individuals like yourself, unfortuantely some of the APIs I would require me to pay monthly fees.

**YouTube:**
If you'd like to watch more of my content, feel free to visit my YouTube channel [Sigma Coding](https://www.youtube.com/c/SigmaCoding).

**Hire Me:**
If you have a project, you think I can help you with feel free to reach out at [coding.sigma@gmail.com](mailto:coding.sigma@gmail.com?subject=[GitHub]%20Project%20Proposal) or fill out the [contract request form](https://forms.office.com/Pages/ResponsePage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAa__aAmF1hURFg5ODdaVTg1TldFVUhDVjJHWlRWRzhZRy4u)
