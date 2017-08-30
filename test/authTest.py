#!/usr/bin/env python
# encoding: utf-8

import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from kkbox_developer_sdk.auth_flow import *
from client import ClientInfo

CLIENT_ID = ClientInfo.client_id
CLIENT_SECRET = ClientInfo.client_secret


class TestAuthSDK(unittest.TestCase):

	def test_fetch_access_token_by_client_credentials(self):
		auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
		auth.fetch_access_token_by_client_credentials()
		access_token = auth.access_token
		assert access_token.access_token != None
		assert access_token.expires_in != None
		assert access_token.token_type != None

if __name__ == '__main__':
    unittest.main()