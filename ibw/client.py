import os
import json
import urllib
import requests
import subprocess
import certifi
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(category=InsecureRequestWarning)
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())


class IBClient():


    def __init__(self, username = None, password = None, account = None):
        '''
            Initalizes a new IBClient Object with the username and password of the
            account holder.
        '''

        # Initalize Client Attributes.
        self.USERNAME = username
        self.PASSWORD = password
        self.ACCOUNT = account
        self.CLIENT_PORTAL_FOLDER = os.path.join(os.getcwd(), r'clientportal.gw')
        self.API_VERSION = 'v1/'

        # Define URL Components
        self.IB_GATEWAY_HOST = r"https://localhost"
        self.IB_GATEWAY_PORT = r"5000"

        # Build the gate way url.
        self.IB_GATEWAY_PATH = self.IB_GATEWAY_HOST + ":" + self.IB_GATEWAY_PORT


    def connect(self):

        # Define components to start server.
        IB_WEB_API_PROC = [r"bin\run.bat", r"root\conf.yaml"]

        # Start the server.
        subprocess.Popen(args = IB_WEB_API_PROC, shell = True, cwd = self.CLIENT_PORTAL_FOLDER, creationflags = subprocess.CREATE_NEW_CONSOLE)

        # redirect to the local host auth window.
        self._auth_redirect()


    def _headers(self, mode = 'json'):
        ''' 
            Returns a dictionary of default HTTP headers for calls to TD Ameritrade API,
            in the headers we defined the Authorization and access token.

            NAME: mode            
            DESC: Defines the content-type for the headers dictionary.
                  default is 'json'. Possible values are ['json','form']
            TYPE: String
        '''

        if mode == 'json':
            headers = {'Content-Type':'application/json'}
        elif mode == 'form':
            headers = {'Content-Type':'application/x-www-form-urlencoded'}

        return headers


    def _build_url(self, endpoint = None):
        '''
            builds a url for a request.

            NAME: endpoint
            DESC: The URL that needs conversion to a full endpoint URL.
            TYPE: String

            RTYPE: String

        '''

        # otherwise build the URL
        return urllib.parse.unquote(urllib.parse.urljoin(self.IB_GATEWAY_PATH, self.API_VERSION) + r'portal/' + endpoint)


    def _make_request(self, endpoint = None, req_type = None, params = None):
        '''
            Handles all the requests made by the client and correctly organizes
            the information so it is sent correctly. Additionally it will also
            build the URL.

            NAME: endpoint
            DESC: The endpoint we wish to request.
            TYPE: String

            NAME: type
            DESC: Defines the type of request to be made. Can be one of four
                  possible values ['GET','POST','DELETE','PUT']
            TYPE: String

            NAME: params
            DESC: Any arguments that are to be sent along in the request. That
                  could be parameters of a 'GET' request, or a data payload of a
                  'POST' request.
            TYPE: Dictionary
    
        '''

        # first build the url
        url = self._build_url(endpoint = endpoint)

        # Scenario 1: POST with a payload.
        if req_type == 'POST'and params is not None:
            
            # make sure it's a JSON String
            headers = self._headers(mode = 'json')

            # grab the response.
            response = requests.post(url, headers = headers, verify = False, data = json.dumps(params))

        # SCENARIO 2: POST without a payload.
        elif req_type == 'POST'and params is None:
            
            # grab the response.
            response = requests.post(url, headers = self._headers(mode = 'json'), verify = False)

        # SCENARIO 3: GET without parameters.
        elif req_type == 'GET' and params is None:

            # grab the response.
            response = requests.get(url, headers = self._headers(mode = 'json'), verify = False)

         # SCENARIO 3: GET with parameters.
        elif req_type == 'GET' and params is not None:

            # grab the response.
            response = requests.get(url, headers = self._headers(mode = 'json'), verify = False, params = params)

        return response 


    def _auth_redirect(self):
        '''
            Opens a new Browser window with the default one specified by the
            operating system. From there will redirect to the URL that the user 
            needs to go to in order to authenticate the newly started session.
        '''

        # Redirect to the URL.
        subprocess.run(["start", self.IB_GATEWAY_PATH], shell=True)

        # wait till they tell us it was successful.
        self._login_success()

        return True


    def _login_success(self):
        '''
            Waits for the user to let the client know that authentication was successful.
        '''

        # Ask the User if the Login was successful.
        login_success = input("If login was successful, please say 'Yes': ")

        if login_success == 'Yes':
            return True
        else:
            return False


    def _prepare_arguments_list(self, parameter_list = None):
        '''
            Some endpoints can take multiple values for a parameter, this
            method takes that list and creates a valid string that can be 
            used in an API request. The list can have either one index or
            multiple indexes.

            NAME: parameter_list
            DESC: A list of paramater values assigned to an argument.
            TYPE: List

            EXAMPLE:
            SessionObject.prepare_arguments_list(parameter_list = ['MSFT', 'SQ'])

        '''

        # validate it's a list.
        if type(parameter_list) is list:

            # specify the delimeter and join the list.            
            delimeter = ','
            parameter_list = delimeter.join(parameter_list)

        return parameter_list


    '''
        SESSION ENDPOINTS
    '''


    def validate(self):
        '''
            Validates the current session for the SSO user.
        '''

        # define request components
        endpoint = r'sso/validate'
        req_type = 'GET'
        content = self._make_request(endpoint = endpoint, req_type = req_type).json()

        return content


    def tickle(self):
        '''
            If the gateway has not received any requests for several minutes an open session will 
            automatically timeout. The tickle endpoint pings the server to prevent the 
            session from ending.
        '''

        # define request components
        endpoint = r'tickle'
        req_type = 'POST'
        content = self._make_request(endpoint = endpoint, req_type = req_type).json()

        return content


    def logout(self):
        '''
            Logs the user out of the gateway session. Any further activity requires 
            re-authentication.
        '''

        # define request components
        endpoint = r'logout'
        req_type = 'POST'
        content = self._make_request(endpoint = endpoint, req_type = req_type).json()

        return content


    def reauthenticate(self):
        '''
            Provides a way to reauthenticate to the Brokerage system as long as there 
            is a valid SSO session, see /sso/validate.
        '''

        # define request components
        endpoint = r'iserver/reauthenticate'
        req_type = 'POST'
        content = self._make_request(endpoint = endpoint, req_type = req_type).json()

        return content


    def is_authenticated(self):
        '''
            Current Authentication status to the Brokerage system. Market Data and 
            Trading is not possible if not authenticated, e.g. authenticated 
            shows false.
        '''

        # define request components
        endpoint = 'iserver/auth/status'
        req_type = 'POST'
        content = self._make_request(endpoint = endpoint, req_type = req_type).json()

        return content


    '''
        MARKET DATA ENDPOINTS
    '''


    def market_data(self, conids = None, since = None, fields = None):
        '''
            Get Market Data for the given conid(s). The end-point will return by 
            default bid, ask, last, change, change pct, close, listing exchange. 
            See response fields for a list of available fields that can be request 
            via fields argument. The endpoint /iserver/accounts should be called 
            prior to /iserver/marketdata/snapshot. To receive all available fields 
            the /snapshot endpoint will need to be called several times.

            NAME: conid
            DESC: The list of contract IDs you wish to pull current quotes for.
            TYPE: List<String>

            NAME: since
            DESC: Time period since which updates are required. 
                  Uses epoch time with milliseconds.
            TYPE: String

            NAME: fields
            DESC: List of fields you wish to retrieve for each quote.
            TYPE: List<String>          

        '''

        # define request components
        endpoint = 'iserver/marketdata/snapshot'
        req_type = 'GET'

        # join the two list arguments so they are both a single string.
        conids_joined = self._prepare_arguments_list(parameter_list = conids)
        
        if fields is not None:
            fields_joined = ",".join(str(n) for n in fields)
        else:
            fields_joined = ""

        # define the parameters
        params = {'conids':conids_joined,
                  'since':since,
                  'fields':fields_joined}

        content = self._make_request(endpoint = endpoint, req_type = req_type, params = params).json()
        return content


    def market_data_history(self, conid = None, period = None, bar = None):
        '''
            Get history of market Data for the given conid, length of data is controlled by period and 
            bar. e.g. 1y period with bar=1w returns 52 data points.

            NAME: conid
            DESC: The contract ID for a given instrument. If you don't know the contract ID use the
                  `search_by_symbol_or_name` endpoint to retrieve it.
            TYPE: String

            NAME: period
            DESC: Specifies the period of look back. For example 1y means looking back 1 year from today.
                  Possible values are ['1d','1w','1m','1y']
            TYPE: String

            NAME: bar
            DESC: Specifies granularity of data. For example, if bar = '1h' the data will be at an hourly level.
                  Possible values are ['5min','1h','1w']
            TYPE: String

        '''

        # define request components
        endpoint = 'iserver/marketdata/history'
        req_type = 'GET'
        params = {'conid':conid, 'period':period, 'bar':bar}
        content = self._make_request(endpoint = endpoint, req_type = req_type, params = params).json()

        return content


    '''
        SERVER ACCOUNTS ENDPOINTS
    '''


    def server_accounts(self):
        '''

            Returns a list of accounts the user has trading access to, their 
            respective aliases and the currently selected account. Note this 
            endpoint must be called before modifying an order or querying 
            open orders.

        '''

        # define request components
        endpoint = 'iserver​/accounts'
        req_type = 'GET'
        content = self._make_request(endpoint = endpoint, req_type = req_type)

        return content


    def update_server_account(self, account_id = None, check = False):
        '''
            If an user has multiple accounts, and user wants to get orders, trades, 
            etc. of an account other than currently selected account, then user 
            can update the currently selected account using this API and then can 
            fetch required information for the newly updated account.

            NAME: account_id
            DESC: The account ID you wish to set for the API Session. This will be used to
                  grab historical data and make orders.
            TYPE: String

        '''

        # define request components
        endpoint = 'iserver/account'
        req_type = 'POST'
        params = {'acctId':account_id}

        if check == False:
            content = self._make_request(endpoint = endpoint, req_type = req_type, params = params).json()
        else:
            content = self._make_request(endpoint = endpoint, req_type = 'GET', params = params).json()

        return content


    def server_accountPNL(self):
        '''
            Returns an object containing PnLfor the selected account and its models 
            (if any).
        '''

        # define request components
        endpoint = 'iserver/account/pnl/partitioned'
        req_type = 'GET'
        content = self._make_request(endpoint = endpoint, req_type = req_type).json()

        return content    

    '''
        CONTRACT ENDPOINTS
    '''

    def symbol_search(self, symbol):
        '''
            Performs a symbol search for a given symbol and returns information related to the
            symbol including the contract id.
        '''

        # define the request components
        endpoint = 'iserver/secdef/search'
        req_type = 'POST'
        payload = {'symbol':symbol}
        content = self._make_request(endpoint = endpoint, req_type = req_type, params= payload).json()

        return content


    '''
        PORTFOLIO ACCOUNTS ENDPOINTS
    '''


    def portfolio_accounts(self):
        '''
            In non-tiered account structures, returns a list of accounts for which the 
            user can view position and account information. This endpoint must be called prior 
            to calling other /portfolio endpoints for those accounts. For querying a list of accounts 
            which the user can trade, see /iserver/accounts. For a list of subaccounts in tiered account 
            structures (e.g. financial advisor or ibroker accounts) see /portfolio/subaccounts.

        '''

        # define request components
        endpoint = 'portfolio/accounts'
        req_type = 'GET'
        content = self._make_request(endpoint = endpoint, req_type = req_type).json()

        return content


    def portfolio_sub_accounts(self):
        '''
            Used in tiered account structures (such as financial advisor and ibroker accounts) to return a 
            list of sub-accounts for which the user can view position and account-related information. This 
            endpoint must be called prior to calling other /portfolio endpoints for those subaccounts. To 
            query a list of accounts the user can trade, see /iserver/accounts.

        '''

        # define request components
        endpoint = r'​portfolio/subaccounts'
        req_type = 'GET'
        content = self._make_request(endpoint = endpoint, req_type = req_type).json()
        
        return content


    def portfolio_account_info(self, account_id = None):
        '''
            Used in tiered account structures (such as financial advisor and ibroker accounts) to return a 
            list of sub-accounts for which the user can view position and account-related information. This 
            endpoint must be called prior to calling other /portfolio endpoints for those subaccounts. To 
            query a list of accounts the user can trade, see /iserver/accounts.

            NAME: account_id
            DESC: The account ID you wish to return info for.
            TYPE: String

        '''

        # define request components
        endpoint = r'portfolio/{}/meta'.format(account_id)
        req_type = 'GET'
        content = self._make_request(endpoint = endpoint, req_type = req_type).json()
        
        return content


    def portfolio_account_summary(self, account_id = None):
        '''
            Returns information about margin, cash balances and other information 
            related to specified account. See also /portfolio/{accountId}/ledger. 
            /portfolio/accounts or /portfolio/subaccounts must be called 
            prior to this endpoint.

            NAME: account_id
            DESC: The account ID you wish to return info for.
            TYPE: String

        '''

        # define request components
        endpoint = r'portfolio/{}/summary'.format(account_id)
        req_type = 'GET'
        content = self._make_request(endpoint = endpoint, req_type = req_type).json()
        
        return content


    def portfolio_account_ledger(self, account_id = None):
        '''
            Information regarding settled cash, cash balances, etc. in the account's 
            base currency and any other cash balances hold in other currencies. /portfolio/accounts 
            or /portfolio/subaccounts must be called prior to this endpoint. The list of supported 
            currencies is available at https://www.interactivebrokers.com/en/index.php?f=3185.

            NAME: account_id
            DESC: The account ID you wish to return info for.
            TYPE: String

        '''

        # define request components
        endpoint = r'portfolio/{}/ledger'.format(account_id)
        req_type = 'GET'
        content = self._make_request(endpoint = endpoint, req_type = req_type).json()
        
        return content


    def portfolio_account_allocation(self, account_id = None):
        '''
            Information about the account's portfolio allocation by Asset Class, Industry and 
            Category. /portfolio/accounts or /portfolio/subaccounts must be called prior to 
            this endpoint.

            NAME: account_id
            DESC: The account ID you wish to return info for.
            TYPE: String

        '''

        # define request components
        endpoint = r'portfolio/{}/allocation'.format(account_id)
        req_type = 'GET'
        content = self._make_request(endpoint = endpoint, req_type = req_type).json()
        
        return content


    def portfolio_accounts_allocation(self, account_ids = None):
        '''
            Similar to /portfolio/{accountId}/allocation but returns a consolidated view of of all the 
            accounts returned by /portfolio/accounts. /portfolio/accounts or /portfolio/subaccounts must 
            be called prior to this endpoint.

            NAME: account_ids
            DESC: A list of Account IDs you wish to return alloacation info for.
            TYPE: List<String>

        '''

        # define request components
        endpoint = r'portfolio/allocation'
        req_type = 'POST'
        payload = account_ids
        content = self._make_request(endpoint = endpoint, req_type = req_type, params = payload).json()
        
        return content


    def portfolio_account_positions(self, account_id = None, page_id = None):
        '''
            Returns a list of positions for the given account. The endpoint supports paging, 
            page's default size is 30 positions. /portfolio/accounts or /portfolio/subaccounts 
            must be called prior to this endpoint.

            NAME: account_id
            DESC: The account ID you wish to return positions for.
            TYPE: String

            NAME: page_id
            DESC: The page you wish to return if there are more than 1. The
                  default value is '0'.
            TYPE: String


            ADDITIONAL ARGUMENTS NEED TO BE ADDED!!!!!
        '''

        # make sure we have a page ID.
        if page_id is None:
            page_id = 0
        else:
            page_id = page_id

        # define request components
        endpoint = r'portfolio/{}/positions/{}'.format(account_id, page_id)
        req_type = 'GET'
        content = self._make_request(endpoint = endpoint, req_type = req_type).json()
        
        return content

    #
    #   RENAME THIS
    #

    def portfolio_account_position(self, account_id = None, conid = None):
        '''
            Returns a list of all positions matching the conid. For portfolio models the conid 
            could be in more than one model, returning an array with the name of the model it 
            belongs to. /portfolio/accounts or /portfolio/subaccounts must be called prior to 
            this endpoint.

            NAME: account_id
            DESC: The account ID you wish to return positions for.
            TYPE: String

            NAME: conid
            DESC: The contract ID you wish to find matching positions for.
            TYPE: String

        '''

        # define request components
        endpoint = r'portfolio/{}/position/{}'.format(account_id, conid)
        req_type = 'GET'
        content = self._make_request(endpoint = endpoint, req_type = req_type).json()

        return content

    #
    #   GET MORE DETAILS ON THIS
    #

    def portfolio_positions_invalidate(self, account_id = None):
        '''
            Invalidates the backend cache of the Portfolio. ???

            NAME: account_id
            DESC: The account ID you wish to return positions for.
            TYPE: String

        '''
        
        # define request components
        endpoint = r'portfolio/{}/positions/invalidate'.format(account_id)
        req_type = 'POST'
        content = self._make_request(endpoint = endpoint, req_type = req_type).json()

        return content


    def portfolio_positions(self, conid = None):
        '''
            Returns an object of all positions matching the conid for all the selected accounts. 
            For portfolio models the conid could be in more than one model, returning an array 
            with the name of the model it belongs to. /portfolio/accounts or /portfolio/subaccounts 
            must be called prior to this endpoint.

            NAME: conid
            DESC: The contract ID you wish to find matching positions for.
            TYPE: String          
        '''

        # define request components
        endpoint = r'portfolio/positions/{}'.format(conid)
        req_type = 'GET'
        content = self._make_request(endpoint = endpoint, req_type = req_type).json()

        return content


    '''
        TRADES ENDPOINTS
    '''


    def trades(self):
        '''
            Returns a list of trades for the currently selected account for current day and 
            six previous days.
        '''

         # define request components
        endpoint = r'iserver/account/trades'
        req_type = 'GET'
        content = self._make_request(endpoint = endpoint, req_type = req_type).json()

        return content


    '''
        ORDERS ENDPOINTS
    '''


    def get_live_orders(self):
        '''
            The end-point is meant to be used in polling mode, e.g. requesting every 
            x seconds. The response will contain two objects, one is notification, the 
            other is orders. Orders is the list of orders (cancelled, filled, submitted) 
            with activity in the current day. Notifications contains information about 
            execute orders as they happen, see status field.

        '''

        # define request components
        endpoint = r'iserver/account/orders'
        req_type = 'GET'
        content = self._make_request(endpoint = endpoint, req_type = req_type).json()

        return content


    def place_order(self, account_id = None, order = None):
        '''
            Please note here, sometimes this end-point alone can't make sure you submit the order 
            successfully, you could receive some questions in the response, you have to to answer 
            them in order to submit the order successfully. You can use "/iserver/reply/{replyid}" 
            end-point to answer questions.

            NAME: account_id
            DESC: The account ID you wish to place an order for.
            TYPE: String

            NAME: order
            DESC: Either an IBOrder object or a dictionary with the specified payload.
            TYPE: IBOrder or Dict

        '''

        if type(order) is dict:
            order = order
        else:
            order = order.create_order()

        # define request components
        endpoint = r'iserver/account/{}/order'.format(account_id)
        req_type = 'POST'
        content = self._make_request(endpoint = endpoint, req_type = req_type, params = order).json()

        return content


    def place_orders(self, account_id = None, orders = None):
        '''
            An extension of the `place_order` endpoint but allows for a list of orders. Those orders may be
            either a list of dictionary objects or a list of IBOrder objects.

            NAME: account_id
            DESC: The account ID you wish to place an order for.
            TYPE: String

            NAME: orders
            DESC: Either a list of IBOrder objects or a list of dictionaries with the specified payload.
            TYPE: List<IBOrder Object> or List<Dictionary>

        '''

        # EXTENDED THIS
        if type(orders) is list:
            orders = orders
        else:
            orders = orders

        # define request components
        endpoint = r'iserver/account/{}/orders'.format(account_id)
        req_type = 'POST'

        try:
            content = self._make_request(endpoint = endpoint, req_type = req_type, params = orders).json()
        except:
            content = self._make_request(endpoint = endpoint, req_type = req_type, params = orders)

        return content

    def place_order_scenario(self, account_id = None, order = None):
        '''
            This end-point allows you to preview order without actually submitting the 
            order and you can get commission information in the response.

            NAME: account_id
            DESC: The account ID you wish to place an order for.
            TYPE: String

            NAME: order
            DESC: Either an IBOrder object or a dictionary with the specified payload.
            TYPE: IBOrder or Dict

        '''

        if type(order) is dict:
            order = order
        else:
            order = order.create_order()

        # define request components
        endpoint = r'iserver/account/{}/order/whatif'.format(account_id)
        req_type = 'POST'

        try:
            content = self._make_request(endpoint = endpoint, req_type = req_type, params = order).json()
        except:
            content = self._make_request(endpoint = endpoint, req_type = req_type, params = order)

        return content


    def modify_order(self, account_id = None, customer_order_id = None, order = None):
        '''
            Modifies an open order. The /iserver/accounts endpoint must first
            be called.

            NAME: account_id
            DESC: The account ID you wish to place an order for.
            TYPE: String

            NAME: customer_order_id
            DESC: The customer order ID for the order you wish to MODIFY.
            TYPE: String

            NAME: order
            DESC: Either an IBOrder object or a dictionary with the specified payload.
            TYPE: IBOrder or Dict

        '''


        if type(order) is dict:
            order = order
        else:
            order = order.create_order()

        # define request components
        endpoint = r'iserver/account/{}/order/{}'.format(account_id, customer_order_id)
        req_type = 'POST'
        content = self._make_request(endpoint = endpoint, req_type = req_type, params = order).json()

        return content 


    def delete_order(self, account_id = None, customer_order_id = None):
        '''
            Deletes the order specified by the customer order ID.

            NAME: account_id
            DESC: The account ID you wish to place an order for.
            TYPE: String

            NAME: customer_order_id
            DESC: The customer order ID for the order you wish to DELETE.
            TYPE: String

        '''
        # define request components
        endpoint = r'iserver/account/{}/order/{}'.format(account_id, customer_order_id)
        req_type = 'DELETE'
        content = self._make_request(endpoint = endpoint, req_type = req_type).json()

        return content 