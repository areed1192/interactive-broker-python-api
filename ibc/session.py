import json
import requests
import logging
import pathlib
import urllib3

from typing import Dict
from urllib3.exceptions import InsecureRequestWarning
from fake_useragent import UserAgent

urllib3.disable_warnings(category=InsecureRequestWarning)

class InteractiveBrokersSession():

    """Serves as the Session for the Interactive Brokers API."""

    def __init__(self, ib_client: object) -> None:
        """Initializes the `InteractiveBrokersSession` client.

        ### Overview
        ----
        The `InteractiveBrokersSession` object handles all the requests made
        for the different endpoints on the Interactive Brokers API.

        ### Parameters
        ----
        client : object
            The `InteractiveBrokersClient` Python Client.

        ### Usage:
        ----
            >>> ib_session = InteractiveBrokersSession()
        """

        from ibc.client import InteractiveBrokersClient

        # We can also add custom formatting to our log messages.
        log_format = '%(asctime)-15s|%(filename)s|%(message)s'

        self.client: InteractiveBrokersClient = ib_client

        self.resource_url = "https://localhost:5000/v1"

        if not pathlib.Path('logs').exists():
            pathlib.Path('logs').mkdir()
            pathlib.Path('logs/log_file_custom.log').touch()

        logging.basicConfig(
            filename="logs/log_file_custom.log",
            level=logging.INFO,
            encoding="utf-8",
            format=log_format
        )

    def build_headers(self) -> Dict:
        """Used to build the headers needed to make the request.

        ### Parameters
        ----
        mode: str, optional
            The content mode the headers is being built for, by default `json`.

        ### Returns
        ----
        Dict:
            A dictionary containing all the components.
        """

        # Fake the headers.
        headers = {
            "Content-Type": "application/json",
            "User-Agent": UserAgent().edge
        }

        return headers

    def build_url(self, endpoint: str) -> str:
        """Build the URL used the make string.

        ### Parameters
        ----
        endpoint : str
            The endpoint used to make the full URL.

        ### Returns
        ----
        str:
            The full URL with the endpoint needed.
        """

        url = self.resource_url + endpoint

        return url

    def make_request(
        self,
        method: str,
        endpoint: str,
        params: dict = None,
        json_payload: dict = None
    ) -> Dict:
        """Handles all the requests in the library.

        ### Overview
        ---
        A central function used to handle all the requests made in the library,
        this function handles building the URL, defining Content-Type, passing
        through payloads, and handling any errors that may arise during the
        request.

        ### Parameters
        ----
        method : str 
            The Request method, can be one of the following: 
            ['get','post','put','delete','patch']

        endpoint : str
            The API URL endpoint, example is 'quotes'

        params : dict (optional, Default={})
            The URL params for the request.

        data : dict (optional, Default={})
        A data payload for a request.

        json_payload : dict (optional, Default={})
            A json data payload for a request

        ### Returns
        ----
        Dict: 
            A Dictionary object containing the 
            JSON values.
        """

        # Build the URL.
        url = self.build_url(endpoint=endpoint)
        headers = self.build_headers()

        logging.info(
            msg="------------------------"
        )

        logging.info(
            msg=f"JSON Payload: {json_payload}"
        )

        logging.info(
            msg=f"Request Method: {method}"
        )

        # Make the request.
        if method == 'post':
            response = requests.post(url=url, params=params, json=json_payload, verify=False, headers=headers)
        elif method == 'get':
            response = requests.get(url=url, params=params, json=json_payload, verify=False, headers=headers)
        elif method == 'delete':
            response = requests.delete(url=url, params=params, json=json_payload, verify=False, headers=headers)

        logging.info(
            msg="URL: {url}".format(url=url)
        )

        logging.info(
            msg=f'Response Status Code: {response.status_code}'
        )

        logging.info(
            msg=f'Response Content: {response.text}'
        )

        # If it's okay and no details.
        if response.ok and len(response.content) > 0:

            return response.json()

        elif len(response.content) > 0 and response.ok:

            return {
                'message': 'response successful',
                'status_code': response.status_code
            }

        elif not response.ok and endpoint =='/api/iserver/account':
            return response.json()

        elif not response.ok:

            if len(response.content) == 0:
                response_data = ''
            else:
                try:
                    response_data = response.json()
                except:
                    response_data = {'content': response.text}

            # Define the error dict.
            error_dict = {
                'error_code': response.status_code,
                'response_url': response.url,
                'response_body': response_data,
                'response_request': dict(response.request.headers),
                'response_method': response.request.method,
            }

            # Log the error.
            logging.error(
                msg=json.dumps(obj=error_dict, indent=4)
            )

            raise requests.HTTPError()
