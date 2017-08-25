#!/usr/bin/env python
# encoding: utf-8

'''
SDK for KKBOX's Open/Partner API. https://docs.kkbox.codes
'''

from fetcher import *
from territory import *


class KKBOXMoodStationFetcher(Fetcher):
    '''
    Get mood stations.

    See `https://docs.kkbox.codes/docs/mood-stations-mood`.
    '''
    @property
    def access_token(self):
        return self.http.access_token

    def __init__(self, access_token):
        self.http = KKBOXHTTP(access_token)

    @assert_access_token
    def fetch_all_mood_stations(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches all mood stations.

        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/mood-stations-mood`.
        '''
        url = 'https://api.kkbox.com/v1.1/mood-stations'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())

    @assert_access_token
    def fetch_mood_station(self, station_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches a mood station by given ID.

        :param station_id: the station ID
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/mood-stations-station`.
        '''
        url = 'https://api.kkbox.com/v1.1/mood-stations/%s' % station_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())