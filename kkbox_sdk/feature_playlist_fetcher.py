#!/usr/bin/env python
# encoding: utf-8

'''
SDK for KKBOX's Open/Partner API. https://docs.kkbox.codes
'''

from fetcher import *
from territory import *


class KKBOXFeaturePlaylistFetcher(Fetcher):
    '''
    List all featured playlists.

    See `https://docs.kkbox.codes/docs/featured-playlists`.
    '''
    @property
    def access_token(self):
        return self.http.access_token

    def __init__(self, access_token):
        self.http = KKBOXHTTP(access_token)

    @assert_access_token
    def fetch_feature_playlists(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches featured playlists.

        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/featured-playlists`.
        '''
        url = 'https://api.kkbox.com/v1.1/featured-playlists'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())