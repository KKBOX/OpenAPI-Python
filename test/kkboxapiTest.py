#!/usr/bin/env python
# encoding: utf-8

import inspect
import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from client import ClientInfo
from kkbox_developer_sdk.auth_flow import *
from kkbox_developer_sdk.api import *

CLIENT_ID = ClientInfo.client_id
CLIENT_SECRET = ClientInfo.client_secret

class TestSDK(unittest.TestCase):

    def test_api_members_exist(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        api = KKBOXAPI(token)
        attributes = inspect.getmembers(api, lambda a:not(inspect.isroutine(a)))
        properties = []
        for (property, _) in attributes:
            properties.append(property)
        members = ('search_fetcher', 'track_fetcher', 'artist_fetcher', 
                   'album_fetcher', 'shared_playlist_fetcher', 'chart_fetcher',
                   'new_release_category_fetcher', 'genre_station_fetcher',
                   'mood_station_fetcher', 'feature_playlist_fetcher', 
                   'feature_playlist_category_fetcher', 'new_hits_playlist_fetcher')
        for member in members:
            assert member in properties, 'missing member ' + member

if __name__ == '__main__':
    unittest.main()