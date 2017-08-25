#!/usr/bin/env python
# encoding: utf-8

'''
SDK for KKBOX's Open/Partner API. https://docs.kkbox.codes
'''

from fetcher import *
from territory import *


class KKBOXTrackFetcher(Fetcher):
    '''
    Get metadata of a track.

    See `https://docs.kkbox.codes/docs/tracks`.
    '''
    @property
    def access_token(self):
        return self.http.access_token

    def __init__(self, access_token):
        self.http = KKBOXHTTP(access_token)

    @assert_access_token
    def fetch_track(self, track_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches a song track by given ID.

        :param track_id: the track ID.
        :type track_id: str
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/tracks`.
        '''
        url = 'https://api.kkbox.com/v1.1/tracks/%s' % track_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())