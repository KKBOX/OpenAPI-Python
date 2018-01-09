#!/usr/bin/env python
# encoding: utf-8
from .fetcher import *
from .territory import *

class KKBOXSharedPlaylistFetcher(Fetcher):
    '''
    Fetch metadata and tracks of a specific shared playlist.

    See `https://docs-en.kkbox.codes/v1.1/reference#shared-playlists`.
    '''
    @assert_access_token
    def fetch_shared_playlist(self, playlist_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches a shared playlist by given ID.

        :param playlist_id: the playlist ID.
        :type playlist_id: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dictcd

        See `https://docs-en.kkbox.codes/v1.1/reference#sharedplaylists-playlist_id`.
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

        See `https://kkbox.gelato.io/docs/versions/1.1/resources/shared-playlists/endpoints/get-shared-playlists-playlist_id-tracks`.
        '''
        url = 'https://api.kkbox.com/v1.1/shared-playlists/%s/tracks' % playlist_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())
