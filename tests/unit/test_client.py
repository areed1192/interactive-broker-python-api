"""Unit test module for the Interactive Brokers Session.

Will perform an instance test to make sure it creates it.
"""

import unittest
import pathlib
import os
import sys
from unittest import TestCase
from ibw.client import IBClient
from typing import List
from configparser import ConfigParser


class InteractiveBrokersSession(TestCase):

    """Will perform a unit test for the Interactive Brokers session."""

    def setUp(self) -> None:
        """Set up the Session."""

        # Grab configuration values.
        config = ConfigParser()
        file_path = pathlib.Path('config/config.ini').resolve()
        config.read(file_path)

        # Load the details.
        self.paper_account = config.get('main','PAPER_ACCOUNT')
        self.paper_username = config.get('main','PAPER_USERNAME')

        # Initalize the Client
        self.ibw_client = IBClient(
            username=self.paper_username,
            account=self.paper_account
        )

    def test_creates_instance_of_session(self):
        """Ensure the instance was created."""

        self.assertIsInstance(self.ibw_client, IBClient)
        self.assertEqual(self.paper_account, self.ibw_client.account)
        self.assertEqual(self.paper_username, self.ibw_client.username)
        self.assertEqual(False, self.ibw_client.authenticated)

    def test_session_properties(self):
        """Checks different session properties."""

        self.assertEqual(self.ibw_client._operating_system, sys.platform)
    
    def test_ibw_portal_path(self):
        """Ensures the Portal Path Matches."""

        folder_path = pathlib.Path('clientportal.beta.gw').resolve()
        self.assertEqual(self.ibw_client.client_portal_folder, folder_path)

    def test_session_state_path(self):
        """Ensures the Session JSON path is valid."""

        session_state_path = pathlib.Path("ibw/server_session.json").resolve()
        self.assertEqual(session_state_path, self.ibw_client.session_state_path)

    def test_create_session(self):
        """Test Creating the session."""

        session_response = self.ibw_client.create_session()
        self.assertTrue(session_response)
        self.assertTrue(self.ibw_client.authenticated)

    def test_close_session(self):
        """Test Closing the session."""
        
        with self.assertRaises(SystemExit) as cm:
            self.ibw_client.close_session()
            self.assertEqual(cm.exception.code, 1)
    
    def tearDown(self) -> None:
        """Teardown the Session."""

        self.ibw_client = None

if __name__ == '__main__':
    unittest.main()
