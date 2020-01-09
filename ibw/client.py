import requests
import urllib
import os
import webbrowser
import subprocess
import ssl

class IBClient():

    def __init__(self, username = None, password = None):

        self.USERNAME = username
        self.PASSWORD = password
        self.CLIENT_PORTAL_FOLDER = os.path.join(os.getcwd(), r'clientportal.gw')
        self.API_VERSION = 'v1/'

        # SSL Issues
        # ssl._create_default_https_context = ssl.create_default_context()

    def connect(self):

        # Define components to start server.
        IB_WEB_API_PATH = self.CLIENT_PORTAL_FOLDER
        IB_WEB_API_PROC = [r"bin\run.bat", r"root\conf.yaml"]

        # Start the server.
        subprocess.Popen(args = IB_WEB_API_PROC, shell = True, cwd = IB_WEB_API_PATH)

        self._auth_redirect()


    def _headers(self):
        headers = {'Content-type':'application/json'}

        return headers

    def _build_url(self, endpoint = None):

        # otherwise build the URL
        return urllib.parse.urljoin(self.IB_GATEWAY_PATH, self.API_VERSION) + endpoint

    def _make_request(self, endpoint = None, type = None, params = None):
        certificate_file = r'C:\Users\305197\Desktop\Repo - IB API\ib-robot\certificate.pem'
        private_key_file = r'C:\Users\305197\Desktop\Repo - IB API\ib-robot\privkey.pem'

        certificate_file = r'C:\Users\305197\Desktop\Repo - IB API\ib-robot\certificate.pem'
        private_key_file = r'C:\Users\305197\Desktop\Repo - IB API\ib-robot\privkey.pem'

        url = self._build_url(endpoint = endpoint)

        if type == 'POST'and params != None:
            response = requests.post(url, headers = self._headers(), cert = (certificate_file, private_key_file), verify = False, data=params)
        elif type == 'POST'and params == None:
            response = requests.post(url, headers = self._headers(), cert = (certificate_file, private_key_file), verify = False)
        elif type == 'GET':
            response = requests.get(url, headers = self._headers(), cert = (certificate_file, private_key_file), verify = False)
            
        return response 

    def _auth_redirect(self):

        # Define URL Components
        IB_GATEWAY_HOST = r"https://localhost"
        IB_GATEWAY_PORT = r"5000"
        self.IB_GATEWAY_PATH = IB_GATEWAY_HOST + ":" + IB_GATEWAY_PORT

        # Redirect to the URL.
        subprocess.run(["start", r'https://localhost:5000'], shell=True)

        self._login_success()

        return True

    def _login_success(self):

        login_success = input("If login was successful, please say 'Yes': ")

        if login_success == 'Yes':
            return True
        else:
            return False

    '''
        SESSION ENDPOINTS
    '''

    def validate(self):
        endpoint = r'/sso/validate'

    def tickle(self):
        endpoint = r'/tickle'

    def logout(self):
        endpoint = r'logout'

    def reauthenticate(self):
        endpoint = r'portal/iserver/reauthenticate'
        response = self._make_request(endpoint = endpoint)
        content_json = response.json()
        return content_json

    def is_authenticated(self):
        endpoint = r'portal/iserver/auth/status'
        response = self._make_request(endpoint = endpoint)
        content_json = response.json()
        print(content_json)

        # if content_json['authenticated'] == False:
        #     content = self.reauthenticate()
        # else:
        #     return True

        # print(content_json)


    '''
        MARKET DATA ENDPOINTS
    '''


    def market_data(self):
        endpoint = r'/iserver/marketdata/snapshot'

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
        endpoint = r'/iserver/marketdata/history'

        params = {'conid':conid,
                  'period':period,
                  'bar':bar}

        content = self._make_request(endpoint = endpoint, type = 'GET', params = params).json()
        return content

    '''
        SERVER ACCOUNTS ENDPOINTS
    '''


    def server_accounts(self):
        endpoint = r'​/iserver​/accounts'
        req_type = 'GET'

    def update_server_account(self):
        endpoint = r'​/iserver​/accounts'
        req_type = 'POST'

    def server_accountPNL(self):
        endpoint = r'/iserver/account/pnl/partitioned'
        req_type = 'POST'


    '''
        PORTFOLIO ACCOUNTS ENDPOINTS
    '''


    def portfolio_accounts(self):
        endpoint = r'​/portfolio​/accounts'
        req_type = 'GET'

    def portfolio_sub_accounts(self):
        endpoint = r'​/portfolio/subaccounts'
        req_type = 'GET'

    def portfolio_account_info(self):
        endpoint = r'/portfolio/{accountId}/meta'
        req_type = 'GET'

    def portfolio_account_summary(self):
        endpoint = r'/portfolio/{accountId}/summary'
        req_type = 'GET'

    def portfolio_account_ledger(self):
        endpoint = r'/portfolio/{accountId}/ledger'
        req_type = 'GET'

    def portfolio_account_allocation(self):
        endpoint = r'/portfolio/allocation'
        req_type = 'GET'

    def portfolio_accounts_allocation(self):
        endpoint = r'/portfolio/allocation'
        req_type = 'POST'

    def portfolio_account_positions(self):
        endpoint = r'/portfolio/{accountId}/positions/{pageId}'
        req_type = 'POST'

    def portfolio_account_position(self):
        endpoint = r'/portfolio/{accountId}/position/{conid}'
        req_type = 'POST'

    def portfolio_positions_invalidate(self):
        endpoint = r'/portfolio/{accountId}/positions/invalidate'
        req_type = 'POST'

    def portfolio_positions(self):
        endpoint = r'/portfolio/positions/{conid}'
        req_type = 'POST'


    '''
        TRADES ENDPOINTS
    '''


    def trades(self):
        endpoint = r'/iserver/account/trades'
        req_type = 'GET'


    '''
        ORDERS ENDPOINTS
    '''


    def get_live_orders(self):
        endpoint = r'/iserver/account/orders'
        req_type = 'GET'

    def place_order(self):
        endpoint = r'/iserver/account/{accountId}/order'
        req_type = 'POST'

    def place_orders(self):
        endpoint = r'/iserver/account/orders'
        req_type = 'POST'

    def place_order_scenario(self):
        endpoint = r'/iserver/account/{accountId}/order/whatif'
        req_type = 'POST'

    def modify_order(self):
        endpoint = r'/iserver/account/{accountId}/order/{origCustomerOrderId}'
        req_type = 'POST'

    def delete_order(self):
        endpoint = r'/iserver/account/{accountId}/order/{origCustomerOrderId}'
        req_type = 'DELETE'


if __name__ == '__main__':

    ib_client = IBClient()
    ib_client.connect()
    ib_client.is_authenticated()