#!/usr/bin/env python
# encoding: utf-8

import sys
import inspect
import os
file_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sdk_path = file_path + '/../kkbox_sdk'
sys.path.append(sdk_path)
from auth_flow import *
from device_flow import *
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

	def test_generate_url_for_getting_auth_code(self):
		auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
		url = auth.generate_url_for_getting_auth_code('http://localhost', 1234)
		print url
		assert url != None
    
	def test_fetch_device_code(self):
		deviceFlow = KKBOXDeviceFlow(CLIENT_ID, CLIENT_SECRET)
		code = deviceFlow.fetch_device_code()
		assert code.device_code != None
		assert code.short_verification_url != None
		assert code.verification_url != None
		assert code.verification_qrcode != None
		assert code.interval != None
		assert code.expires_in != None
		assert code.user_code != None


if __name__ == '__main__':
    unittest.main()