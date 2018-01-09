#!/usr/bin/env python
# encoding: utf-8
from .fetcher import *
from .territory import *

class KKBOXFeaturePlaylistFetcher(Fetcher):
    '''
    List all featured playlists metadata.

    See `https://docs-en.kkbox.codes/v1.1/reference#featured-playlists`.
    '''
    @assert_access_token
    def fetch_all_feature_playlists(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches featured playlists.

        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs-en.kkbox.codes/v1.1/reference#featuredplaylists`.
        '''
        url = 'https://api.kkbox.com/v1.1/featured-playlists'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())

    @assert_access_token
    def fetch_feature_playlist(self, playlist_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches featured playlists.

        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs-en.kkbox.codes/v1.1/reference#featuredplaylists-playlist_id`.
        '''
        url = 'https://api.kkbox.com/v1.1/featured-playlists/%s' % playlist_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())

    @assert_access_token
    def fetch_feature_playlist_tracks(self, playlist_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches featured playlists.

        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs-en.kkbox.codes/v1.1/reference#featuredplaylists-playlist_id-tracks`.
        '''
        url = 'https://api.kkbox.com/v1.1/featured-playlists/%s/tracks' % playlist_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())
