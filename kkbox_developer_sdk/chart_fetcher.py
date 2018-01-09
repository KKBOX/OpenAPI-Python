#!/usr/bin/env python
# encoding: utf-8
from .fetcher import *
from .territory import *

class KKBOXChartFetcher(Fetcher):
    '''
    List chart playlist. Then can get tracks via shared playlist.

    See `https://docs-en.kkbox.codes/v1.1/reference#charts`.
    '''
    @assert_access_token
    def fetch_charts(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches list of song rankings.

        :param terr: the current territory.
        :return: API response.
        :rtype: list

        See `https://docs-en.kkbox.codes/v1.1/reference#charts_1`
        '''
        url = 'https://api.kkbox.com/v1.1/charts'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())

    @assert_access_token
    def fetch_charts_playlist(self, playlist_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches chart categories.

        :param terr: the current territory.
        :return: API response.
        :rtype: list

        See `https://docs-en.kkbox.codes/v1.1/reference#charts-playlist_id`
        '''
        url = 'https://api.kkbox.com/v1.1/charts/%s' % playlist_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())

    @assert_access_token
    def fetch_charts_playlist_tracks(self, playlist_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches chart categories.

        :param terr: the current territory.
        :return: API response.
        :rtype: list

        See `https://docs-en.kkbox.codes/v1.1/reference#charts-playlist_id-tracks`
        '''
        url = 'https://api.kkbox.com/v1.1/charts/%s/tracks' % playlist_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())
