#!/usr/bin/env python
# encoding: utf-8
from .fetcher import *
from .territory import *

class KKBOXTrackFetcher(Fetcher):
    '''
    Get metadata of a track.

    See `https://docs-en.kkbox.codes/v1.1/reference#tracks`.
    '''
    @assert_access_token
    def fetch_track(self, track_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches a song track by given ID.

        :param track_id: the track ID.
        :type track_id: str
        :return: API response.
        :rtype: dict

        See `https://docs-en.kkbox.codes/v1.1/reference#tracks-track_id`.
        '''
        url = 'https://api.kkbox.com/v1.1/tracks/%s' % track_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())
