#!/usr/bin/env python
# encoding: utf-8

import sys
import inspect
import os
file_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sdk_path = file_path + '/../kkbox_sdk'
sys.path.append(sdk_path)
from auth_flow import *
from client import ClientInfo

CLIENT_ID = ClientInfo.client_id
CLIENT_SECRET = ClientInfo.client_secret
AUTH_CODE = ClientInfo.auth_code


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