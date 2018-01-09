#!/usr/bin/env python
# encoding: utf-8
from .fetcher import *
from .territory import *

class KKBOXNewHitsPlaylistFetcher(Fetcher):
    '''
    List all new hits playlists and fetch tracks for specific new hit playlist.

    See 'https://docs-en.kkbox.codes/v1.1/reference#new-hits-playlists'.
    '''
    @assert_access_token
    def fetch_all_new_hits_playlists(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches all new hits playlists.

        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See 'https://docs-en.kkbox.codes/v1.1/reference#newhitsplaylists'
        '''
        url = 'https://api.kkbox.com/v1.1/new-hits-playlists'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())

    @assert_access_token
    def fetch_new_hits_playlist(self, playlist_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches new hits playlist by given ID.

        :param playlist_id: the playlist ID.
        :type playlist_id: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See 'https://docs-en.kkbox.codes/v1.1/reference#newhitsplaylists-playlist_id'
        '''
        url = 'https://api.kkbox.com/v1.1/new-hits-playlists/%s' % playlist_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())

    @assert_access_token
    def fetch_new_hits_playlist_tracks(self, playlist_id, terr= KKBOXTerritory.TAIWAN):
        '''
        Fetches new hits playlist by given ID.

        :param playlist_id: the playlist ID.
        :type playlist_id: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See 'https://docs-en.kkbox.codes/v1.1/reference#newhitsplaylists-playlist_id-tracks'
        '''
        url = 'https://api.kkbox.com/v1.1/new-hits-playlists/%s/tracks' % playlist_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())
