#!/usr/bin/env python
# encoding: utf-8

'''
SDK for KKBOX's Open/Partner API. https://docs.kkbox.codes
'''

from fetcher import *
from territory import *


class KKBOXNewHitsPlaylistFetcher(Fetcher):
    '''
    List new hits playhits.

    See 'https://docs.kkbox.codes/docs/new-hits-playlists'.
    '''
    @property
    def access_token(self):
        return self.http.access_token

    def __init__(self, access_token):
        self.http = KKBOXHTTP(access_token)

    @assert_access_token
    def fetch_all_new_hits_playlists(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches all new hits playlists.

        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See 'https://docs.kkbox.codes/docs/new-hits-playlists'
        '''
        url = 'https://api.kkbox.com/v1.1/new-hits-playlists'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())

    @assert_access_token
    def fetch_new_hits_playlist(self, playlist_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches new hits playlist by given ID.

        :param playlist_id: the category.
        :type playlist_id: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See 'https://docs.kkbox.codes/docs/new-hits-playlists-playlist-id'
        '''
        url = 'https://api.kkbox.com/v1.1/new-hits-playlists/%s' % playlist_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())