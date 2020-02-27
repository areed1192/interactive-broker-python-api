import os
import sys
import json
import time
import pathlib
import urllib
import requests
import subprocess

import urllib3
import certifi
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(category=InsecureRequestWarning)
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

TESTING_FLAG_ALEX = True

class IBClient():


    def __init__(self, username = None, password = None, account = None):
        '''
            Initalizes a new IBClient Object with the username and password of the
            account holder.
        '''
        
        self.ACCOUNT = account
        self.USERNAME = username
        self.PASSWORD = password
        self.CLIENT_PORTAL_FOLDER = pathlib.Path.cwd().joinpath('clientportal.gw').resolve()
        self.API_VERSION = 'v1/'
        self.TESTING_FLAG = False
        self._operating_system = sys.platform
        self.server_process = self._server_state(action ='load')
        self.authenticated = False

        # Define URL Components
        IB_GATEWAY_HOST = r"https://localhost"
        IB_GATEWAY_PORT = r"5000"
        self.IB_GATEWAY_PATH = IB_GATEWAY_HOST + ":" + IB_GATEWAY_PORT

    def _check_server_update(self):

        server_update_content = self.update_server_account(account_id = self.ACCOUNT, check = False)

        if 'set' in server_update_content.keys() and server_update_content['set'] == True:
            print('')
            print('New session has been created and authenticated. Requests will not be limited.'.upper())
            print('')
            return True
        elif ('message' in server_update_content.keys()) and (server_update_content['message'] == 'Account already set'):
            print('')
            print('New session has been created and authenticated. Requests will not be limited.'.upper())
            print('')
            return True      
        else:
            print('')
            print('Could not create a new session that was authenticated, exiting script.'.upper())
            print('')
            sys.exit()

    def create_session(self):
        '''
            Creates a new session with Interactive Broker using the credentials
            passed through when the Robot was initalized.
        '''
           
        # first let's check if the server is running, if it's not then we can start up.
        if self.server_process == None and self.connect():
            
            # then make sture the server is updated.
            if self._check_server_update():
                return True

        # more than likely it's running let's try and see if we can authenticate.
        auth_response = self.is_authenticated()

        if 'authenticated' in auth_response.keys() and auth_response['authenticated'] == True:
            
            self.authenticated == True

            if self._check_server_update():
                return True

        else:
                 
            # in this case don't connect, but prompt the user to log in again.
            self.connect(start_server=False)

            if self._check_server_update():
                return True

    def _server_state(self, action = 'save'):
        '''
            Maintains the server state, so we can easily load a previous session,
            save a new session, or delete a closed session.

            NAME: action
            DESC: The action you wish to take to the `json` file. Can be one of the following options:
                    1. save - saves the current state and overwrites the old one.
                    2. load - loads the previous state from a session that has a server still running.
                    3. delete - deletes the state because the server has been closed.
            TYPE: String

            RTYPE: None | Integer
        '''

        dir_path = os.path.dirname(os.path.realpath(__file__))
        filename = 'server_session.json'
        file_path = os.path.join(dir_path, filename)
        file_exists = os.path.exists(file_path)

        if action == 'save':
            with open(file_path, 'w') as server_file:
                json.dump({'server_process_id':self.server_process},server_file)

        elif action == 'load' and file_exists:

            with open(file_path, 'r') as server_file:
                server_state = json.load(server_file)

            try:
                os.kill(server_state['server_process_id'], 0)
            except OSError:
                return server_state['server_process_id']
            except SystemError:
                return server_state['server_process_id']
            else:
               return None

        elif action == 'delete' and file_exists:
            os.remove(file_path)
        else:
            return None

    def connect(self, start_server = True):
        '''
            Connects the session to the Interactive Broker API by, starting up the Client Portal Gateway,
            prompting the user to log in and then returns the results back to the `create_session` method.

            RTYPE: BOOLEAN
        '''

        if start_server:
            # windows will use the command line application.
            if self._operating_system == 'win32':
                IB_WEB_API_PROC = ["cmd", "/k", r"bin\run.bat", r"root\conf.yaml"]
                self.server_process = subprocess.Popen(args = IB_WEB_API_PROC, cwd = self.CLIENT_PORTAL_FOLDER, creationflags = subprocess.CREATE_NEW_CONSOLE).pid

            # mac will use the terminal.
            elif self._operating_system == 'darwin':
                IB_WEB_API_PROC = ["open", "-F", "-a", "Terminal", r"bin/run.sh", r"root/conf.yaml"]
                self.server_process = subprocess.Popen(args = IB_WEB_API_PROC, cwd = self.CLIENT_PORTAL_FOLDER).pid

        self._server_state(action='save')

        print('''{}
        The Interactive Broker server is currently starting up, so we can authenticate your session.
            STEP 1: GO TO THE FOLLOWING URL: {}
            STEP 2: LOGIN TO YOUR ACCOUNT WITH YOUR USERNAME AND PASSWORD.
            STEP 3: WHEN YOU SEE `Client login succeeds` RETURN BACK TO THE TERMINAL AND TYPE `YES` TO CHECK IF THE SESSION IS AUTHENTICATED.
            SERVER IS RUNNING ON PROCESS ID: {}
        {}
        '''.format('-'*80, self.IB_GATEWAY_PATH, self.server_process, '-'*80)
        )

        while self.authenticated == False:

            user_input = input('Would you like to make an authenticated request (Yes/No)? ').upper()

            if user_input == 'NO':
                self.close_session
            else:
                auth_response = self.is_authenticated()

            if 'statusCode' in auth_response.keys() and auth_response['statusCode'] == 401:
                self.authenticated = False
            elif 'authenticated' in auth_response.keys() and auth_response['authenticated'] == True:
                self.authenticated = True

        return True

    def close_session(self):

        print('\nCLOSING SERVER AND EXITING SCRIPT.')
        return_code = subprocess.call("TASKKILL /F /PID {} /T".format(self.server_process), creationflags=subprocess.DETACHED_PROCESS)
        self._server_state(action ='delete')
        sys.exit()

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
            # headers['accept'] = 'application/json'
            # headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'

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
            headers = self._headers(mode = 'json')
            # headers['accept'] = 'application/json'
            response = requests.get(url, headers = headers, verify = False, params = params)

        # grab the status code
        if response.status_code != 200:
            print(response.url)
            print(response.headers)
            print(response.content)
            print(response.status_code)
            
        return response 


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

        # this is special, I don't want the JSON content right away.
        content = self._make_request(endpoint = endpoint, req_type = req_type)

        if content.status_code != 200:
            return False
        else:
            return content.json()
            

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
        if since is None:
            params = {'conids':conids_joined,
                      'fields':fields_joined}
        else:
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
        endpoint = 'iserver/accounts'
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

        content = self._make_request(endpoint = endpoint, req_type = req_type, params = params).json()

        if 'status_code' in content.keys():
            time.sleep(1)
            content = self._make_request(endpoint = endpoint, req_type = req_type, params = params).json()

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