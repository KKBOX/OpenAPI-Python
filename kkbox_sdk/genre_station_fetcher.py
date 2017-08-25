#!/usr/bin/env python
# encoding: utf-8

'''
SDK for KKBOX's Open/Partner API. https://docs.kkbox.codes
'''

from fetcher import *
from territory import *


class KKBOXGenreStationFetcher(Fetcher):
    '''
    Get genre stations.

    See `https://docs.kkbox.codes/docs/genre-stations-genre`.
    '''
    @property 
    def access_token(self):
        return self.http.access_token

    def __init__(self, access_token):
        self.http = KKBOXHTTP(access_token)

    @assert_access_token
    def fetch_all_genre_stations(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches all genre stations.

        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/genre-stations-genre`.
        '''
        url = 'https://api.kkbox.com/v1.1/genre-stations'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())

    @assert_access_token
    def fetch_genre_station(self, station_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches a genre station by given ID.

        :param station_id: the station ID
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/genre-stations-station`.
        '''
        url = 'https://api.kkbox.com/v1.1/genre-stations/%s' % station_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())