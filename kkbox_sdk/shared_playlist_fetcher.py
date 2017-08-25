#!/usr/bin/env python
# encoding: utf-8

'''
SDK for KKBOX's Open/Partner API. https://docs.kkbox.codes
'''

from fetcher import *
from territory import *


class KKBOXSharedPlaylistFetcher(Fetcher):
    '''
    Get plylist metadata.

    See `https://docs.kkbox.codes/docs/shared-playlists`.
    '''
    @property
    def access_token(self):
        return self.http.access_token

    def __init__(self, access_token):
        self.http = KKBOXHTTP(access_token)

    @assert_access_token
    def fetch_shared_playlist(self, playlist_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches a shared playlist by given ID.

        :param playlist_id: the playlist ID.
        :type playlist_id: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dictcd

        See `https://docs.kkbox.codes/docs/shared-playlists`.
        '''
        url = 'https://api.kkbox.com/v1.1/shared-playlists/%s' % playlist_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())
    
    @assert_access_token
    def fetch_tracks_of_shared_playlists(self, playlist_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches track list of a playlist by given ID.

        :param playlist_id: the playlist ID.
        :type playlist_id: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/shared-playlistsplaylist_idtrackss`.
        '''
        url = 'https://api.kkbox.com/v1.1/shared-playlists/%s/tracks' % playlist_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())