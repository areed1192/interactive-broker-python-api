import os
import sys
import ssl
import json
import time
import urllib
import urllib3
import certifi
import logging
import pathlib
import requests
import textwrap
import subprocess

from typing import Union
from typing import List
from typing import Dict

from urllib3.exceptions import InsecureRequestWarning
from ibw.clientportal import ClientPortal

urllib3.disable_warnings(category=InsecureRequestWarning)
# http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

logging.basicConfig(
    filename='app.log',
    format='%(levelname)s - %(name)s - %(message)s',
    level=logging.DEBUG
)


class IBClient():

    def __init__(self, username: str, account: str, client_gateway_path: str = None, is_server_running: bool = True) -> None:
        """Initalizes a new instance of the IBClient Object.

        Arguments:
        ----
        username {str} -- Your IB account username for either your paper or regular account.

        account {str} -- Your IB account number for either your paper or regular account.

        Keyword Arguments:
        ----
        password {str} -- Your IB account password for either your paper or regular account. (default:{""})

        Usage:
        ----
            >>> ib_paper_session = IBClient(
                username='IB_PAPER_USERNAME',
                account='IB_PAPER_ACCOUNT',
            )
            >>> ib_paper_session
            >>> ib_regular_session = IBClient(
                username='IB_REGULAR_USERNAME',
                account='IB_REGULAR_ACCOUNT',
            )
            >>> ib_regular_session
        """

        self.account = account
        self.username = username
        self.client_portal_client = ClientPortal()

        self.api_version = 'v1/'
        self._operating_system = sys.platform
        self.session_state_path: pathlib.Path = pathlib.Path(__file__).parent.joinpath('server_session.json').resolve()
        self.authenticated = False
        self._is_server_running = is_server_running

        # Define URL Components
        ib_gateway_host = r"https://localhost"
        ib_gateway_port = r"5000"
        self.ib_gateway_path = ib_gateway_host + ":" + ib_gateway_port
        self.backup_gateway_path = r"https://cdcdyn.interactivebrokers.com/portal.proxy"
        self.login_gateway_path = self.ib_gateway_path + "/sso/Login?forwardTo=22&RL=1&ip2loc=on"


        if client_gateway_path is None:

            # Grab the Client Portal Path.
            self.client_portal_folder: pathlib.Path = pathlib.Path(__file__).parents[1].joinpath(
                'resources/clientportal.beta.gw'
            ).resolve()

            # See if it exists.
            if not self.client_portal_folder.exists() and not self._is_server_running:
                print("The Client Portal Gateway doesn't exist. You need to download it before using the Library.")
                print("Downloading the Client Portal file...")
                self.client_portal_client.download_and_extract()
                        
        else:

            self.client_portal_folder = client_gateway_path

        if not self._is_server_running:

            # Load the Server State.
            self.server_process = self._server_state(action='load')

            # Log the initial Info.
            logging.info(textwrap.dedent('''
            =================
            Initialize Client:
            =================
            Server Process: {serv_proc}
            Operating System: {op_sys}
            Session State Path: {state_path}
            Client Portal Folder: {client_path}
            ''').format(
                    serv_proc=self.server_process,
                    op_sys=self._operating_system,
                    state_path=self.session_state_path,
                    client_path=self.client_portal_folder
                )
            )
        else:
            self.server_process = None


    def create_session(self, set_server=True) -> bool:
        """Creates a new session.

        Creates a new session with Interactive Broker using the credentials
        passed through when the Robot was initalized.

        Usage:
        ----
            >>> ib_client = IBClient(
                username='IB_PAPER_username',
                password='IB_PAPER_PASSWORD',
                account='IB_PAPER_account',
            )
            >>> server_response = ib_client.create_session()
            >>> server_response
                True

        Returns:
        ----
        bool -- True if the session was created, False if wasn't created.
        """

        # first let's check if the server is running, if it's not then we can start up.
        if self.server_process is None and not self._is_server_running:

            # If it's None we need to connect first.
            if set_server:
                self.connect(start_server=True, check_user_input=True)
            else:
                self.connect(start_server=True, check_user_input=False)
                return True

            # then make sure the server is updated.
            if self._set_server():
                return True

        # Try and authenticate.
        auth_response = self.is_authenticated()

        # Log the initial Info.
        logging.info(textwrap.dedent('''
        =================
        Create Session:
        =================
        Auth Response: {auth_resp}
        ''').format(
                auth_resp=auth_response,
            )
        )

        # Finally make sure we are authenticated.
        if 'authenticated' in auth_response.keys() and auth_response['authenticated'] and self._set_server():
            self.authenticated = True
            return True
        else:
            # In this case don't connect, but prompt the user to log in again.
            self.connect(start_server=False)
            
            if self._set_server():
                self.authenticated = True
                return True

    def _set_server(self) -> bool:
        """Sets the server info for the session.

        Sets the Server for the session, and if the server cannot be set then
        script will halt. Otherwise will return True to continue on in the script.

        Returns:
        ----
        bool -- True if the server was set, False if wasn't
        """
        success = '\nNew session has been created and authenticated. Requests will not be limited.\n'.upper()
        failure = '\nCould not create a new session that was authenticated, exiting script.\n'.upper()

        # Grab the Server accounts.
        server_account_content = self.server_accounts()

        # Try to do the quick way.
        if (server_account_content and 'accounts' in server_account_content):
            accounts = server_account_content['accounts']
            if self.account in accounts:

                # Log the response.
                logging.debug(textwrap.dedent('''
                =================
                Set Server:
                =================
                Server Response: {serv_resp}
                ''').format(
                        serv_resp=server_account_content
                    )
                )

                print(success)
                return True
        else:

            # Update the Server.
            server_update_content = self.update_server_account(
                account_id=self.account,
                check=False
            )

            # Grab the accounts.
            server_account_content = self.server_accounts()

            # Log the response.
            logging.debug(textwrap.dedent('''
            =================
            Set Server:
            =================
            Server Response: {serv_resp}
            Server Update Response: {auth_resp}
            ''').format(
                    auth_resp=server_update_content,
                    serv_resp=server_account_content
                )
            )

            # TO DO: Add check market hours here and then check for a mutual fund.
            if (server_account_content and 'accounts' in server_account_content) or (server_update_content and 'message' in server_update_content):
                print(success)
                return True
            else:
                print(failure)
                sys.exit()

        # # TO DO: Add check market hours here and then check for a mutual fund.
        # news = self.data_news(conid='265598')
        # if news and 'news' in news:
        #     print(success)
        #     return True
        # if server_account_content is not None and 'set' in server_update_content.keys() and server_update_content['set'] == True:
        #     print(success)
        #     return True
        # elif ('message' in server_update_content.keys()) and (server_update_content['message'] == 'Account already set'):
        #     print(success)
        #     return True
        # else:
        #     print(failure)
        #     sys.exit()

    def _server_state(self, action: str = 'save') -> Union[None, int]:
        """Determines the server state.

        Maintains the server state, so we can easily load a previous session,
        save a new session, or delete a closed session.

        Arguments:
        ----
        action {str} -- The action you wish to take to the `json` file. Can be one of the following options:

        1. save - saves the current state and overwrites the old one.
        2. load - loads the previous state from a session that has a server still running.
        3. delete - deletes the state because the server has been closed.

        Returns:
        ----
        Union[None, int] -- The Process ID of the Server.
        """

        # Define file components.
        file_exists = self.session_state_path.exists()

        # Log the response.
        logging.debug(textwrap.dedent('''
        =================
        Server State:
        =================
        Server State: {state}
        State File: {exist}
        ''').format(
                state=action,
                exist=file_exists
            )
        )

        if action == 'save':

            # Save the State.
            with open(self.session_state_path, 'w') as server_file:
                json.dump(
                    obj={'server_process_id': self.server_process},
                    fp=server_file
                )

        # If we are loading check the file exists first.
        elif action == 'load' and file_exists:

            try:
                self.is_authenticated(check=True)
                check_proc_id = False
            except:
                check_proc_id = True

            # Load it.
            with open(self.session_state_path, 'r') as server_file:
                server_state = json.load(fp=server_file)

            # Grab the Process Id.
            proc_id = server_state['server_process_id']

            # If it's running return the process ID.
            if check_proc_id:
                is_running = self._check_if_server_running(process_id=proc_id)
            else:
                is_running = True

            if is_running:
                return proc_id

        # Delete it.
        elif action == 'delete' and file_exists:
            self.session_state_path.unlink()

    def _check_if_server_running(self, process_id: str) -> bool:
        """Used to see if the Clientportal Gateway is running.

        Arguments:
        ----
        process_id (str): The process ID of the clientportal.

        Returns:
        ----
        bool: `True` if running, `False` otherwise.
        """

        if self._operating_system == 'win32':

            # See if the Process is running.
            with os.popen('tasklist') as task_list:

                # Grab each task.
                for process in task_list.read().splitlines()[4:]:

                    if str(process_id) in process:

                        # Log the response.
                        logging.debug(textwrap.dedent('''
                            =================
                            Server Process:
                            =================
                            Process ID: {process}
                            ''').format(
                                process=process
                            )
                        )

                        return True

        else:

            try:
                os.kill(process_id, 0)
                return True
            except OSError:
                return False

    def _check_authentication_user_input(self) -> bool:
        """Used to check the authentication of the Server.

        Returns:
        ----
        bool: `True` if authenticated, `False` otherwise.
        """

        max_retries = 0
        while (max_retries > 4 or self.authenticated == False):
            
            # Grab the User Request.
            user_input = input(
                'Would you like to make an authenticated request (Yes/No)? '
            ).upper()

            # If no, close the session.
            if user_input == 'NO':
                self.close_session()
            # Else try and see if we are authenticated.
            else:
                auth_response = self.is_authenticated(check=True)

            # Log the Auth Response.
            logging.debug('Check User Auth Inital: {auth_resp}'.format(
                    auth_resp=auth_response
                )
            )

            if 'statusCode' in auth_response.keys() and auth_response['statusCode'] == 401:
                print("Session isn't connected, closing script.")
                self.close_session()

            elif 'authenticated' in auth_response.keys() and auth_response['authenticated'] == True:
                self.authenticated = True
                break

            elif 'authenticated' in auth_response.keys() and auth_response['authenticated'] == False:
                valid_resp = self.validate()
                reauth_resp = self.reauthenticate()
                auth_response = self.is_authenticated()

                try:
                    serv_resp = self.server_accounts()
                    if 'accounts' in serv_resp:
                        self.authenticated = True

                        # Log the response.
                        logging.debug('Had to do Server Account Request: {auth_resp}'.format(
                                auth_resp=serv_resp
                            )
                        )
                        break
                except:
                    pass

                logging.debug(
                    '''
                    Validate Response: {valid_resp}
                    Reauth Response: {reauth_resp}
                    '''.format(
                        valid_resp=valid_resp,
                        reauth_resp=reauth_resp
                    )
                )

            max_retries += 1

        return self.authenticated

    def _check_authentication_non_input(self) -> bool:
        """Runs the authentication protocol but without user input.

        Returns:
        ----
        bool: `True` if authenticated, `False` otherwise.
        """

        # Grab the auth response.
        auth_response = self.is_authenticated(check=True)

        # Log the Auth response.
        logging.debug('Check Non-User Auth Inital: {auth_resp}'.format(
                auth_resp=auth_response
            )
        )

        # Fail early, status code means we can't authenticate.
        if 'statusCode' in auth_response:
            print("Session isn't connected, closing script.")
            self.close_session()

        # Grab the Auth Response Flag.
        auth_response_value = auth_response.get('authenticated', None)

        # If it it's True we are good.
        if auth_response_value:
            self.authenticated = True

        # If not, try and reauthenticate.
        elif not auth_response_value:

            # Validate the session first.
            self.validate()

            # Then reauthenticate the session.
            reauth_response = self.reauthenticate()

            # See if it was triggered.
            if 'message' in reauth_response:
                self.authenticated = True
            else:
                self.authenticated = False

    def _start_server(self) -> str:
        """Starts the Server.

        Returns:
        ----
        str: The Server Process ID.
        """

        # windows will use the command line application.
        if self._operating_system == 'win32':
            IB_WEB_API_PROC = ["cmd", "/k", r"bin\run.bat", r"root\conf.yaml"]
            self.server_process = subprocess.Popen(
                args=IB_WEB_API_PROC,
                cwd=self.client_portal_folder,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            ).pid

        # mac will use the terminal.
        elif self._operating_system == 'darwin':
            IB_WEB_API_PROC = [
                "open", "-F", "-a",
                "Terminal", r"bin/run.sh", r"root/conf.yaml"
            ]
            self.server_process = subprocess.Popen(
                args=IB_WEB_API_PROC,
                cwd=self.client_portal_folder
            ).pid

        return self.server_process

    def connect(self, start_server: bool = True, check_user_input: bool = True) -> bool:
        """Connects the session with the API.

        Connects the session to the Interactive Broker API by, starting up the Client Portal Gateway,
        prompting the user to log in and then returns the results back to the `create_session` method.

        Arguments:
        ----
        start_server {bool} -- True if the server isn't running but needs to be started, False if it
            is running and just needs to be authenticated.

        Returns:
        ----
        bool -- `True` if it was connected.
        """

        logging.debug('Running Client Folder at: {file_path}'.format(
            file_path=self.client_portal_folder))

        # If needed, start the server and save the State.
        if start_server:
            self._start_server()
            self._server_state(action='save')

        # Display prompt if needed.
        if check_user_input:

            print(textwrap.dedent("""{lin_brk}
            The Interactive Broker server is currently starting up, so we can authenticate your session.
                STEP 1: GO TO THE FOLLOWING URL: {url}
                STEP 2: LOGIN TO YOUR account WITH YOUR username AND PASSWORD.
                STEP 3: WHEN YOU SEE `Client login succeeds` RETURN BACK TO THE TERMINAL AND TYPE `YES` TO CHECK IF THE SESSION IS AUTHENTICATED.
                SERVER IS RUNNING ON PROCESS ID: {proc_id}
            {lin_brk}""".format(
                        lin_brk='-'*80,
                        url=self.login_gateway_path,
                        proc_id=self.server_process
                    )
                )
            )

            # Check the auth status
            auth_status = self._check_authentication_user_input()

        else:

            auth_status = True

        return auth_status

    def close_session(self) -> None:
        """Closes the current session and kills the server using Taskkill."""

        print('\nCLOSING SERVER AND EXITING SCRIPT.')

        # Define the process.
        process = "TASKKILL /F /PID {proc_id} /T".format(
            proc_id=self.server_process
        )

        # Kill the process.
        subprocess.call(process, creationflags=subprocess.DETACHED_PROCESS)

        # Delete the state
        self._server_state(action='delete')

        # and exit.
        sys.exit()

    def _headers(self, mode: str = 'json') -> Dict:
        """Builds the headers.

        Returns a dictionary of default HTTP headers for calls to Interactive 
        Brokers API, in the headers we defined the Authorization and access 
        token.

        Arguments:
        ----
        mode {str} -- Defines the content-type for the headers dictionary.
            default is 'json'. Possible values are ['json','form']

        Returns:
        ----
        Dict
        """

        if mode == 'json':
            headers = {
                'Content-Type': 'application/json'
            }
        elif mode == 'form':
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        elif mode == 'none':
            headers = None

        return headers

    def _build_url(self, endpoint: str) -> str:
        """Builds a url for a request.

        Arguments:
        ----
        endpoint {str} -- The URL that needs conversion to a full endpoint URL.

        Returns:
        ----
        {srt} -- A full URL path.
        """

        # otherwise build the URL
        return urllib.parse.unquote(
            urllib.parse.urljoin(
                self.ib_gateway_path,
                self.api_version
            ) + r'portal/' + endpoint
        )

    def _make_request(self, endpoint: str, req_type: str, headers: str = 'json', params: dict = None, data: dict = None, json: dict = None) -> Dict:
        """Handles the request to the client.

        Handles all the requests made by the client and correctly organizes
        the information so it is sent correctly. Additionally it will also
        build the URL.

        Arguments:
        ----
        endpoint {str} -- The endpoint we wish to request.

        req_type {str} --  Defines the type of request to be made. Can be one of four
            possible values ['GET','POST','DELETE','PUT']

        params {dict} -- Any arguments that are to be sent along in the request. That
            could be parameters of a 'GET' request, or a data payload of a
            'POST' request.

        Returns:
        ----
        {Dict} -- A response dictionary.

        """
        # First build the url.
        url = self._build_url(endpoint=endpoint)

        # Define the headers.
        headers = self._headers(mode=headers)

        # Make the request.
        if req_type == 'POST':
            response = requests.post(url=url, headers=headers, params=params, json=json, verify=False)
        elif req_type == 'GET':
            response = requests.get(url=url, headers=headers, params=params, json=json, verify=False)
        elif req_type == 'DELETE':
            response = requests.delete(url=url, headers=headers, params=params, json=json, verify=False)

        # grab the status code
        status_code = response.status_code

        # grab the response headers.
        response_headers = response.headers
        
        # Check to see if it was successful
        if response.ok:

            if response_headers.get('Content-Type','null') == 'application/json;charset=utf-8':
                data = response.json()
            else:
                data = response.json()

            # Log it.
            logging.debug('''
            Response Text: {resp_text}
            Response URL: {resp_url}
            Response Code: {resp_code}
            Response JSON: {resp_json}
            Response Headers: {resp_headers}
            '''.format(
                    resp_text=response.text,
                    resp_url=response.url,
                    resp_code=status_code,
                    resp_json=data,
                    resp_headers=response_headers
                )
            )

            return data

        # if it was a bad request print it out.
        elif not response.ok and url != 'https://localhost:5000/v1/portal/iserver/account':
            print(url)
            raise requests.HTTPError()

    def _prepare_arguments_list(self, parameter_list: List[str]) -> str:
        """Prepares the arguments for the request.

        Some endpoints can take multiple values for a parameter, this
        method takes that list and creates a valid string that can be
        used in an API request. The list can have either one index or
        multiple indexes.

        Arguments:
        ----
        parameter_list {List} -- A list of paramater values assigned to an argument.

        Usage:
        ----
            >>> SessionObject._prepare_arguments_list(parameter_list=['MSFT','SQ'])

        Returns:
        ----
        {str} -- The joined list.

        """

        # validate it's a list.
        if type(parameter_list) is list:

            # specify the delimiter and join the list.
            delimiter = ','
            parameter_list = delimiter.join(parameter_list)

        return parameter_list

    """
        SESSION ENDPOINTS
    """

    def validate(self) -> Dict:
        """Validates the current session for the SSO user."""

        # define request components
        endpoint = r'sso/validate'
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def tickle(self) -> Dict:
        """Keeps the session open.

        If the gateway has not received any requests for several minutes an open session will 
        automatically timeout. The tickle endpoint pings the server to prevent the 
        session from ending.
        """

        # define request components
        endpoint = r'tickle'
        req_type = 'POST'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def logout(self) -> Dict:
        """Logs the session out.

        Overview:
        ----
        Logs the user out of the gateway session. Any further 
        activity requires re-authentication.

        Returns:
        ----
        (dict): A logout response.
        """

        # Define request components.
        endpoint = r'logout'
        req_type = 'POST'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def reauthenticate(self) -> Dict:
        """Reauthenticates an existing session.

        Overview:
        ----
        Provides a way to reauthenticate to the Brokerage 
        system as long as there is a valid SSO session, 
        see /sso/validate.

        Returns:
        ----
        (dict): A reauthentication response.        
        """

        # Define request components.
        endpoint = r'iserver/reauthenticate'
        req_type = 'POST'

        # Make the request.
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def is_authenticated(self, check: bool = False) -> Dict:
        """Checks if session is authenticated.

        Overview:
        ----
        Current Authentication status to the Brokerage system. Market Data and 
        Trading is not possible if not authenticated, e.g. authenticated 
        shows `False`.

        Returns:
        ----
        (dict): A dictionary with an authentication flag.   
        """

        # define request components
        endpoint = 'iserver/auth/status'

        if not check:
            req_type = 'POST'
        else:
            req_type = 'GET'

        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            headers='none'
        )

        return content

    def _fundamentals_summary(self, conid: str) -> Dict:
        """Grabs a financial summary of a company.

        Return a financial summary for specific Contract ID. The financial summary
        includes key ratios and descriptive components of the Contract ID.

        Arguments:
        ----        
        conid {str} -- The contract ID.

        Returns:
        ----
        {Dict} -- The response dictionary.
        """

        # define request components
        endpoint = 'iserver/fundamentals/{}/summary'.format(conid)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def _fundamentals_financials(self, conid: str, financial_statement: str, period: str = 'annual') -> Dict:
        """Grabs fundamental financial data.

        Overview:
        ----
        Return a financial summary for specific Contract ID. The financial summary
        includes key ratios and descriptive components of the Contract ID.

        Arguments:
        ----
        conid (str): The contract ID.

        financial_statement (str): The specific financial statement you wish to request 
            for the Contract ID. Possible values are ['balance','cash','income']

        period (str, optional): The specific period you wish to see. 
            Possible values are ['annual','quarter']. Defaults to 'annual'.

        Returns:
        ----
        Dict: Financial data for the specified contract ID.
        """

        # define the period
        if period == 'annual':
            period = True
        else:
            period = False

        # Build the arguments.
        params = {
            'type': financial_statement,
            'annual': period
        }

        # define request components
        endpoint = 'tws.proxy/fundamentals/financials/{}'.format(conid)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            params=params
        )

        return content

    def _fundamentals_key_ratios(self, conid: str) -> Dict:
        """Returns analyst ratings for a specific conid.

            NAME: conid
            DESC: The contract ID.
            TYPE: String
        """

        # Build the arguments.
        params = {
            'widgets': 'key_ratios'
        }

        # define request components
        endpoint = 'fundamentals/landing/{}'.format(conid)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            params=params
        )

        return content

    def _fundamentals_dividends(self, conid: str) -> Dict:
        """Returns analyst ratings for a specific conid.

        NAME: conid
        DESC: The contract ID.
        TYPE: String
        """

        # Build the arguments.
        params = {
            'widgets': 'dividends'
        }

        # define request components
        endpoint = 'fundamentals/landing/{}'.format(conid)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            params=params
        )

        return content

    def _fundamentals_esg(self, conid: str) -> Dict:
        """
            Returns analyst ratings for a specific conid.

            NAME: conid
            DESC: The contract ID.
            TYPE: String

        """

        # Build the arguments.
        params = {
            'widgets': 'esg'
        }

        # define request components
        endpoint = 'fundamentals/landing/{}'.format(conid)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            params=params
        )

        return content

    def _data_news(self, conid: str) -> Dict:
        """
            Return a financial summary for specific Contract ID. The financial summary
            includes key ratios and descriptive components of the Contract ID.

            NAME: conid
            DESC: The contract ID.
            TYPE: String
        """

        # Build the arguments.
        params = {
            'widgets': 'news',
            'lang': 'en'
        }

        # define request components
        endpoint = 'fundamentals/landing/{}'.format(conid)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            params=params
        )

        return content

    def _data_ratings(self, conid: str) -> Dict:
        """Returns analyst ratings for a specific conid.

        NAME: conid
        DESC: The contract ID.
        TYPE: String
        """

        # Build the arguments.
        params = {
            'widgets': 'ratings'
        }

        # define request components
        endpoint = 'fundamentals/landing/{}'.format(conid)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            params=params
        )

        return content

    def _data_events(self, conid: str) -> Dict:
        """Returns analyst ratings for a specific conid.

        NAME: conid
        DESC: The contract ID.
        TYPE: String
        """

        # Build the arguments.
        params = {
            'widgets': 'ratings'
        }

        # define request components
        endpoint = 'fundamentals/landing/{}'.format(conid)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            params=params
        )

        return content

    def _data_ownership(self, conid: str) -> Dict:
        """Returns analyst ratings for a specific conid.

        NAME: conid
        DESC: The contract ID.
        TYPE: String
        """

        # Build the arguments.
        params = {
            'widgets': 'ownership'
        }

        # define request components
        endpoint = 'fundamentals/landing/{}'.format(conid)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            params=params
        )

        return content

    def _data_competitors(self, conid: str) -> Dict:
        """Returns analyst ratings for a specific conid.

        NAME: conid
        DESC: The contract ID.
        TYPE: String
        """

        # Build the arguments.
        params = {
            'widgets': 'competitors'
        }

        # define request components
        endpoint = 'fundamentals/landing/{}'.format(conid)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            params=params
        )

        return content

    def _data_analyst_forecast(self, conid: str) -> Dict:
        """Returns analyst ratings for a specific conid.

        NAME: conid
        DESC: The contract ID.
        TYPE: String
        """

        # Build the arguments.
        params = {
            'widgets': 'analyst_forecast'
        }

        # define request components
        endpoint = 'fundamentals/landing/{}'.format(conid)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            params=params
        )

        return content

    def market_data(self, conids: List[str], since: str, fields: List[str]) -> Dict:
        """
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
        """

        # define request components
        endpoint = 'iserver/marketdata/snapshot'
        req_type = 'GET'

        # join the two list arguments so they are both a single string.
        conids_joined = self._prepare_arguments_list(parameter_list=conids)

        if fields is not None:
            fields_joined = ",".join(str(n) for n in fields)
        else:
            fields_joined = ""

        # define the parameters
        if since is None:
            params = {
                'conids': conids_joined,
                'fields': fields_joined
            }
        else:
            params = {
                'conids': conids_joined,
                'since': since,
                'fields': fields_joined
            }

        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            params=params
        )

        return content

    def market_data_history(self, conid: str, period: str, bar: str) -> Dict:
        """
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
        """

        # define request components
        endpoint = 'iserver/marketdata/history'
        req_type = 'GET'
        params = {
            'conid': conid,
            'period': period,
            'bar': bar
        }

        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            params=params
        )

        return content

    def server_accounts(self):
        """
            Returns a list of accounts the user has trading access to, their
            respective aliases and the currently selected account. Note this
            endpoint must be called before modifying an order or querying
            open orders.
        """

        # define request components
        endpoint = 'iserver/accounts'
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def update_server_account(self, account_id: str, check: bool = False) -> Dict:
        """
            If an user has multiple accounts, and user wants to get orders, trades, 
            etc. of an account other than currently selected account, then user 
            can update the currently selected account using this API and then can 
            fetch required information for the newly updated account.

            NAME: account_id
            DESC: The account ID you wish to set for the API Session. This will be used to
                  grab historical data and make orders.
            TYPE: String
        """

        # define request components
        endpoint = 'iserver/account'
        req_type = 'POST'
        params = {
            'acctId': account_id
        }

        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            params=params
        )

        return content

    def server_account_pnl(self):
        """
        Returns an object containing PnLfor the selected account and its models 
        (if any).
        """

        # define request components
        endpoint = 'iserver/account/pnl/partitioned'
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def symbol_search(self, symbol: str) -> Dict:
        """
            Performs a symbol search for a given symbol and returns 
            information related to the symbol including the contract id.
        """

        # define the request components
        endpoint = 'iserver/secdef/search'
        req_type = 'POST'
        payload = {
            'symbol': symbol
        }

        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            json=payload
        )

        return content

    def contract_details(self, conid: str) -> Dict:
        """
            Get contract details, you can use this to prefill your order before you submit an order.

            NAME: conid
            DESC: The contract ID you wish to get details for.
            TYPE: String

            RTYPE: Dictionary
        """

        # define the request components
        endpoint = '/iserver/contract/{conid}/info'.format(conid=conid)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def contracts_definitions(self, conids: List[str]) -> Dict:
        """
            Returns a list of security definitions for the given conids.

            NAME: conids
            DESC: A list of contract IDs you wish to get details for.
            TYPE: List<Integer>

            RTYPE: Dictionary
        """

        # Define the request components.
        endpoint = '/trsrv/secdef'
        req_type = 'POST'
        payload = {
            'conids': conids
        }

        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            json=payload
        )

        return content

    def futures_search(self, symbols: List[str]) -> Dict:
        """
            Returns a list of non-expired future contracts for given symbol(s).

            NAME: Symbol
            DESC: List of case-sensitive symbols separated by comma.
            TYPE: List<String>

            RTYPE: Dictionary
        """

        # define the request components
        endpoint = '/trsrv/futures'
        req_type = 'GET'
        params = {
            'symbols': '{}'.format(','.join(symbols))
        }

        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            params=params
        )

        return content

    def symbols_search_list(self, symbols: List[str]) -> Dict:
        """
            Returns a list of non-expired future contracts for given symbol(s).

            NAME: Symbol
            DESC: List of case-sensitive symbols separated by comma.
            TYPE: List<String>

            RTYPE: Dictionary
        """

        # define the request components
        endpoint = '/trsrv/stocks'
        req_type = 'GET'
        params = {'symbols': '{}'.format(','.join(symbols))}
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            params=params
        )

        return content

    def portfolio_accounts(self):
        """
            In non-tiered account structures, returns a list of accounts for which the 
            user can view position and account information. This endpoint must be called prior 
            to calling other /portfolio endpoints for those accounts. For querying a list of accounts 
            which the user can trade, see /iserver/accounts. For a list of subaccounts in tiered account 
            structures (e.g. financial advisor or ibroker accounts) see /portfolio/subaccounts.

        """

        # define request components
        endpoint = 'portfolio/accounts'
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def portfolio_sub_accounts(self):
        """
            Used in tiered account structures (such as financial advisor and ibroker accounts) to return a 
            list of sub-accounts for which the user can view position and account-related information. This 
            endpoint must be called prior to calling other /portfolio endpoints for those subaccounts. To 
            query a list of accounts the user can trade, see /iserver/accounts.

        """

        # define request components
        endpoint = r'​portfolio/subaccounts'
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def portfolio_account_info(self, account_id: str) -> Dict:
        """
            Used in tiered account structures (such as financial advisor and ibroker accounts) to return a 
            list of sub-accounts for which the user can view position and account-related information. This 
            endpoint must be called prior to calling other /portfolio endpoints for those subaccounts. To 
            query a list of accounts the user can trade, see /iserver/accounts.

            NAME: account_id
            DESC: The account ID you wish to return info for.
            TYPE: String
        """

        # define request components
        endpoint = r'portfolio/{}/meta'.format(account_id)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def portfolio_account_summary(self, account_id: str) -> Dict:
        """
            Returns information about margin, cash balances and other information 
            related to specified account. See also /portfolio/{accountId}/ledger. 
            /portfolio/accounts or /portfolio/subaccounts must be called 
            prior to this endpoint.

            NAME: account_id
            DESC: The account ID you wish to return info for.
            TYPE: String
        """

        # define request components
        endpoint = r'portfolio/{}/summary'.format(account_id)
        req_type = 'GET'
        content = self._make_request(endpoint=endpoint, req_type=req_type)

        return content

    def portfolio_account_ledger(self, account_id: str) -> Dict:
        """
            Information regarding settled cash, cash balances, etc. in the account's 
            base currency and any other cash balances hold in other currencies. /portfolio/accounts 
            or /portfolio/subaccounts must be called prior to this endpoint. The list of supported 
            currencies is available at https://www.interactivebrokers.com/en/index.php?f=3185.

            NAME: account_id
            DESC: The account ID you wish to return info for.
            TYPE: String
        """

        # define request components
        endpoint = r'portfolio/{}/ledger'.format(account_id)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def portfolio_account_allocation(self, account_id: str) -> Dict:
        """
            Information about the account's portfolio allocation by Asset Class, Industry and 
            Category. /portfolio/accounts or /portfolio/subaccounts must be called prior to 
            this endpoint.

            NAME: account_id
            DESC: The account ID you wish to return info for.
            TYPE: String
        """

        # define request components
        endpoint = r'portfolio/{}/allocation'.format(account_id)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def portfolio_accounts_allocation(self, account_ids: List[str]) -> Dict:
        """
            Similar to /portfolio/{accountId}/allocation but returns a consolidated view of of all the 
            accounts returned by /portfolio/accounts. /portfolio/accounts or /portfolio/subaccounts must 
            be called prior to this endpoint.

            NAME: account_ids
            DESC: A list of Account IDs you wish to return alloacation info for.
            TYPE: List<String>
        """

        # define request components
        endpoint = r'portfolio/allocation'
        req_type = 'POST'
        payload = account_ids
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            json=payload
        )

        return content

    def portfolio_account_positions(self, account_id: str, page_id: int = 0) -> Dict:
        """
            Returns a list of positions for the given account. The endpoint supports paging, 
            page's default size is 30 positions. /portfolio/accounts or /portfolio/subaccounts 
            must be called prior to this endpoint.

            NAME: account_id
            DESC: The account ID you wish to return positions for.
            TYPE: String

            NAME: page_id
            DESC: The page you wish to return if there are more than 1. The
                  default value is `0`.
            TYPE: String

            ADDITIONAL ARGUMENTS NEED TO BE ADDED!!!!!
        """

        # define request components
        endpoint = r'portfolio/{}/positions/{}'.format(account_id, page_id)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def portfolio_account_position(self, account_id: str, conid: str) -> Dict:
        """
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
        """

        # Define request components.
        endpoint = r'portfolio/{}/position/{}'.format(account_id, conid)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def portfolio_positions_invalidate(self, account_id: str) -> Dict:
        """
            Invalidates the backend cache of the Portfolio. ???

            NAME: account_id
            DESC: The account ID you wish to return positions for.
            TYPE: String
        """

        # Define request components.
        endpoint = r'portfolio/{}/positions/invalidate'.format(account_id)
        req_type = 'POST'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def portfolio_positions(self, conid: str) -> Dict:
        """
            Returns an object of all positions matching the conid for all the selected accounts. 
            For portfolio models the conid could be in more than one model, returning an array 
            with the name of the model it belongs to. /portfolio/accounts or /portfolio/subaccounts 
            must be called prior to this endpoint.

            NAME: conid
            DESC: The contract ID you wish to find matching positions for.
            TYPE: String          
        """

        # Define request components.
        endpoint = r'portfolio/positions/{}'.format(conid)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def trades(self):
        """
            Returns a list of trades for the currently selected account for current day and 
            six previous days.
        """

        # define request components
        endpoint = r'iserver/account/trades'
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def get_live_orders(self):
        """
            The end-point is meant to be used in polling mode, e.g. requesting every 
            x seconds. The response will contain two objects, one is notification, the 
            other is orders. Orders is the list of orders (cancelled, filled, submitted) 
            with activity in the current day. Notifications contains information about 
            execute orders as they happen, see status field.
        """

        # define request components
        endpoint = r'iserver/account/orders'
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def place_order(self, account_id: str, order: dict) -> Dict:
        """
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
        """

        if type(order) is dict:
            order = order
        else:
            order = order.create_order()

        # define request components
        endpoint = r'iserver/account/{}/order'.format(account_id)
        req_type = 'POST'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            json=order
        )

        return content

    def place_orders(self, account_id: str, orders: List[Dict]) -> Dict:
        """
            An extension of the `place_order` endpoint but allows for a list of orders. Those orders may be
            either a list of dictionary objects or a list of IBOrder objects.

            NAME: account_id
            DESC: The account ID you wish to place an order for.
            TYPE: String

            NAME: orders
            DESC: Either a list of IBOrder objects or a list of dictionaries with the specified payload.
            TYPE: List<IBOrder Object> or List<Dictionary>
        """

        # EXTENDED THIS
        if type(orders) is list:
            orders = orders
        else:
            orders = orders

        # define request components
        endpoint = r'iserver/account/{}/orders'.format(account_id)
        req_type = 'POST'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            json=orders
        )

        return content

    def place_order_scenario(self, account_id: str, order: dict) -> Dict:
        """
            This end-point allows you to preview order without actually submitting the 
            order and you can get commission information in the response.

            NAME: account_id
            DESC: The account ID you wish to place an order for.
            TYPE: String

            NAME: order
            DESC: Either an IBOrder object or a dictionary with the specified payload.
            TYPE: IBOrder or Dict
        """

        if type(order) is dict:
            order = order
        else:
            order = order.create_order()

        # define request components
        endpoint = r'iserver/account/{}/order/whatif'.format(account_id)
        req_type = 'POST'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            json=order
        )

        return content

    def place_order_reply(self, reply_id: str = None, reply: str = None):
        """
            An extension of the `place_order` endpoint but allows for a list of orders. Those orders may be
            either a list of dictionary objects or a list of IBOrder objects.

            NAME: account_id
            DESC: The account ID you wish to place an order for.
            TYPE: String

            NAME: orders
            DESC: Either a list of IBOrder objects or a list of dictionaries with the specified payload.
            TYPE: List<IBOrder Object> or List<Dictionary>
        """

        # define request components
        endpoint = r'iserver/reply/{}'.format(reply_id)
        req_type = 'POST'
        reply = {
            'confirmed': reply
        }

        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            json=reply
        )

        return content

    def modify_order(self, account_id: str, customer_order_id: str, order: dict) -> Dict:
        """
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
        """

        if type(order) is dict:
            order = order
        else:
            order = order.create_order()

        # define request components
        endpoint = r'iserver/account/{}/order/{}'.format(
            account_id, customer_order_id)
        req_type = 'POST'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            json=order
        )

        return content

    def delete_order(self, account_id: str, customer_order_id: str) -> Dict:
        """Deletes the order specified by the customer order ID.

        NAME: account_id
        DESC: The account ID you wish to place an order for.
        TYPE: String

        NAME: customer_order_id
        DESC: The customer order ID for the order you wish to DELETE.
        TYPE: String
        """

        # define request components
        endpoint = r'iserver/account/{}/order/{}'.format(
            account_id, customer_order_id)
        req_type = 'DELETE'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def get_scanners(self):
        """Returns an object contains four lists contain all parameters for scanners.

        RTYPE Dictionary
        """
        # define request components
        endpoint = r'iserver/scanner/params'
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def run_scanner(self, instrument: str, scanner_type: str, location: str, size: str = '25', filters: List[dict] = None) -> Dict:
        """Run a scanner to get a list of contracts.

        NAME: instrument
        DESC: The type of financial instrument you want to scan for.
        TYPE: String

        NAME: scanner_type
        DESC: The Type of scanner you wish to run, defined by the scanner code.
        TYPE: String

        NAME: location
        DESC: The geographic location you wish to run the scan. For example (STK.US.MAJOR)
        TYPE: String

        NAME: size
        DESC: The number of results to return back. Defaults to 25.
        TYPE: String

        NAME: filters
        DESC: A list of dictionaries where the key is the filter you wish to set and the value is the value you want set
            for that filter.
        TYPE: List<Dictionaries>

        RTYPE Dictionary
        """

        # define request components
        endpoint = r'iserver/scanner/run'
        req_type = 'POST'
        payload = {
            "instrument": instrument,
            "type": scanner_type,
            "filter": filters,
            "location": location,
            "size": size
        }

        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            json=payload
        )

        return content

    def customer_info(self) -> Dict:
        """Returns Applicant Id with all owner related entities     

        RTYPE Dictionary
        """

        # define request components
        endpoint = r'ibcust/entity/info'
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def get_unread_messages(self) -> Dict:
        """Returns the unread messages associated with the account.

        RTYPE Dictionary
        """

        # define request components
        endpoint = r'fyi/unreadnumber'
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def get_subscriptions(self) -> Dict:
        """Return the current choices of subscriptions, we can toggle the option.

        RTYPE Dictionary
        """

        # define request components
        endpoint = r'fyi/settings'
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def change_subscriptions_status(self, type_code: str, enable: bool = True) -> Dict:
        """Turns the subscription on or off.

        NAME: type_code
        DESC: The subscription code you wish to change the status for.
        TYPE: String

        NAME: enable
        DESC: True if you want the subscription turned on, False if you want it turned of.
        TYPE: Boolean

        RTYPE Dictionary
        """

        # define request components
        endpoint = r'fyi/settings/{}'
        req_type = 'POST'
        payload = {'enable': enable}
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            json=payload
        )

        return content

    def subscriptions_disclaimer(self, type_code: str) -> Dict:
        """Returns the disclaimer for the specified subscription.

        NAME: type_code
        DESC: The subscription code you wish to change the status for.
        TYPE: String

        RTYPE Dictionary
        """

        # define request components
        endpoint = r'fyi/disclaimer/{}'
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def mark_subscriptions_disclaimer(self, type_code: str) -> Dict:
        """Sets the specified disclaimer to read.

        NAME: type_code
        DESC: The subscription code you wish to change the status for.
        TYPE: String

        RTYPE Dictionary
        """

        # define request components
        endpoint = r'fyi/disclaimer/{}'
        req_type = 'PUT'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def subscriptions_delivery_options(self):
        """Options for sending fyis to email and other devices.

        RTYPE Dictionary
        """

        # define request components
        endpoint = r'fyi/deliveryoptions'
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def mutual_funds_portfolios_and_fees(self, conid: str) -> Dict:
        """Grab the Fees and objectives for a specified mutual fund.

        NAME: conid
        DESC: The Contract ID for the mutual fund.
        TYPE: String

        RTYPE Dictionary
        """

        # define request components
        endpoint = r'fundamentals/mf_profile_and_fees/{mutual_fund_id}'.format(
            mutual_fund_id=conid)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type
        )

        return content

    def mutual_funds_performance(self, conid: str, risk_period: str, yield_period: str, statistic_period: str) -> Dict:
        """Grab the Lip Rating for a specified mutual fund.

        NAME: conid
        DESC: The Contract ID for the mutual fund.
        TYPE: String

        NAME: yield_period
        DESC: The Period threshold for yield information
                possible values: ['6M', '1Y', '3Y', '5Y', '10Y']
        TYPE: String

        NAME: risk_period
        DESC: The Period threshold for risk information
                possible values: ['6M', '1Y', '3Y', '5Y', '10Y']
        TYPE: String

        NAME: statistic_period
        DESC: The Period threshold for statistic information
                possible values: ['6M', '1Y', '3Y', '5Y', '10Y']
        TYPE: String

        RTYPE Dictionary
        """

        # define request components
        endpoint = r'fundamentals/mf_performance/{mutual_fund_id}'.format(
            mutual_fund_id=conid)
        req_type = 'GET'
        params = {
            'risk_period': None,
            'yield_period': None,
            'statistic_period': None
        }
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            params=params
        )

        return content
