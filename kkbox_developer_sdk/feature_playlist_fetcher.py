#!/usr/bin/env python
# encoding: utf-8
from fetcher import *
from territory import *

class KKBOXFeaturePlaylistFetcher(Fetcher):
    '''
    List all featured playlists metadata.

    See `https://kkbox.gelato.io/docs/versions/1.1/resources/featured-playlists`.
    '''
    @assert_access_token
    def fetch_feature_playlists(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches featured playlists.

        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://kkbox.gelato.io/docs/versions/1.1/resources/featured-playlists/endpoints/get-featured-playlists`.
        '''
        url = 'https://api.kkbox.com/v1.1/featured-playlists'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())