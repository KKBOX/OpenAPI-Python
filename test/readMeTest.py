import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

class TestReadMe(unittest.TestCase):
    def testReadMeExample(self):
        from kkbox_developer_sdk.auth_flow import KKBOXOAuth
        from client import ClientInfo
        auth = KKBOXOAuth(ClientInfo.client_id, ClientInfo.client_secret)
        token = auth.fetch_access_token_by_client_credentials()
        from kkbox_developer_sdk.api import KKBOXAPI
        kkboxapi = KKBOXAPI(token)
        artist_id = '8q3_xzjl89Yakn_7GB'
        artist = kkboxapi.artist_fetcher.fetch_artist(artist_id)
        assert(artist != None)

if __name__ == '__main__':
    unittest.main()