#!/usr/bin/env python
# encoding: utf-8
from fetcher import *
from territory import *

class KKBOXChartFetcher(Fetcher):
    '''
    List chart playlist. Then can get tracks via shared playlist.

    See `https://kkbox.gelato.io/docs/versions/1.1/resources/charts`.
    '''
    @assert_access_token
    def fetch_charts(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches chart categories.

        :param terr: the current territory.
        :return: API response.
        :rtype: list

        See `https://kkbox.gelato.io/docs/versions/1.1/resources/charts/endpoints/get-charts`
        '''
        url = 'https://api.kkbox.com/v1.1/charts'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())