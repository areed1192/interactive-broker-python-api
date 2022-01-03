# Unofficial Interactive Brokers API

## Table of Contents

- [Overview](#overview)
- [What's in the API](#whats-in-the-api)
- [Requirements](#requirements)
- [Usage](#usage)
- [Documentation & Resources](#documentation-and-resources)
- [Support These Projects](#support-these-projects)

## Overview

The unofficial Python API client library for Interactive Broker Client Portal Web API allows individuals with Interactive Broker accounts to manage trades, pull historical and real-time data, manage their accounts, create and modify orders all using the Python programming language.

Interactive Broker offers multiple APIs for their clients. If you would like to learn more about their API offerings click on the links below:

- Trade Workstation API, please refer to the [official documentation](http://interactivebrokers.github.io/tws-api/)
- Client Portal API, please refer to the [official documentation](https://interactivebrokers.github.io/cpwebapi/)
- Third Party API, plesfe refer to the [official documentation](https://www.interactivebrokers.com/webtradingapi/)

## Requirements

The following requirements must be met to use this API:

- A Interactive Broker account, you'll need your account password and account number to use the API.
- [Java 8](https://developers.redhat.com/products/openjdk/download) update 192 or higher installed (gateway is compatible with higher Java versions including OpenJDK 11).
- Download the [Beta Client Portal Gateway](https://www.interactivebrokers.com/en/index.php?f=45185)

## Setup

**Setup - Requirements Install:***

For this particular project, you only need to install the dependencies, to use the project. The dependencies
are listed in the `requirements.txt` file and can be installed by running the following command:

```console
pip install -r requirements.txt
```

After running that command, the dependencies should be installed.

**Setup - Local Install:**

If you are planning to make modifications to this project or you would like to access it
before it has been indexed on `PyPi`. I would recommend you either install this project
in `editable` mode or do a `local install`. For those of you, who want to make modifications
to this project. I would recommend you install the library in `editable` mode.

If you want to install the library in `editable` mode, make sure to run the `setup.py`
file, so you can install any dependencies you may need. To run the `setup.py` file,
run the following command in your terminal.

```console
pip install -e .
```

If you don't plan to make any modifications to the project but still want to use it across
your different projects, then do a local install.

```console
pip install .
```

This will install all the dependencies listed in the `setup.py` file. Once done
you can use the library wherever you want.

<!-- **Setup - PyPi Install:**

To **install** the library, run the following command from the terminal.

```console
pip install federal-register
```

**Setup - PyPi Upgrade:**

To **upgrade** the library, run the following command from the terminal.

```console
pip install --upgrade federal-register
``` -->

## Documentation and Resources

- [Getting Started](https://interactivebrokers.github.io/cpwebapi/index.html#login)
- [Endpoints](https://interactivebrokers.com/api/doc.html)
- [Websockets](https://interactivebrokers.github.io/cpwebapi/RealtimeSubscription.html)

## Usage

Here is a simple example of using the `ibc-api` library.

```python
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

# Grab the Auth Service.
auth_service = ibc_client.authentication

# Login
auth_service.login()

# check if we are authenticated.
pprint(
    auth_service.is_authenticated()
)

# Validate the current session.
pprint(
    auth_service.sso_validate()
)
```

## Support These Projects

**Patreon:**
Help support this project and future projects by donating to my [Patreon Page](https://www.patreon.com/sigmacoding). I'm
always looking to add more content for individuals like yourself, unfortuantely some of the APIs I would require me to
pay monthly fees.

**YouTube:**
If you'd like to watch more of my content, feel free to visit my YouTube channel [Sigma Coding](https://www.youtube.com/c/SigmaCoding).
