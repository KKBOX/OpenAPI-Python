#!/usr/bin/env python
# encoding: utf-8

import sys

sys.path.append('../')
from kkbox_sdk import *
from client import ClientInfo

CLIENT_ID = ClientInfo.client_id
CLIENT_SECRET = ClientInfo.client_secret


class TestAuthSDK(unittest.TestCase):

	def test_fetch_access_token_by_client_credentials(self):
		sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
		sdk.fetch_access_token_by_client_credentials()
		access_token = sdk.access_token
		assert access_token.access_token != None
		assert access_token.expires_in != None
		assert access_token.token_type != None

	def test_generate_url_for_getting_auth_code(self):
		sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
		url = sdk.generate_url_for_getting_auth_code('http://localhost', 1234)
		assert url != None
    
	def test_fetch_device_code(self):
		sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
		code = sdk.fetch_device_code()
		assert code.device_code != None
		assert code.short_verification_url != None
		assert code.verification_url != None
		assert code.verification_qrcode != None
		assert code.interval != None
		assert code.expires_in != None
		assert code.user_code != None


if __name__ == '__main__':
    unittest.main()