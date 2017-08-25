#!/usr/bin/env python
# encoding: utf-8

'''
SDK for KKBOX's Open/Partner API. https://docs.kkbox.codes
'''

from fetcher import *
from territory import *


class KKBOXChartFetcher(Fetcher):
    '''
    List chart playlist. Then can get tracks via shared playlist.

    See `https://docs.kkbox.codes/docs/charts`.
    '''
    @property
    def access_token(self):
        return self.http.access_token

    def __init__(self, access_token):
        self.http = KKBOXHTTP(access_token)

    @assert_access_token
    def fetch_charts(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches chart categories.

        :param terr: the current territory.
        :return: API response.
        :rtype: list

        See `https://docs.kkbox.codes/docs/charts`
        '''
        url = 'https://api.kkbox.com/v1.1/charts'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())