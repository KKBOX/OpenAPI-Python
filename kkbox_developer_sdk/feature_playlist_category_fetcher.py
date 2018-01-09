#!/usr/bin/env python
# encoding: utf-8
from .fetcher import *
from .territory import *

class KKBOXFeaturePlaylistCategoryFetcher(Fetcher):
    '''
    List feature playlist categories and list feature playlists for a specific category.

    See `https://docs-en.kkbox.codes/v1.1/reference#featured-playlist-categories`.
    '''
    @assert_access_token
    def fetch_categories_of_feature_playlist(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches categories of featured playlist.

        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs-en.kkbox.codes/v1.1/reference#featuredplaylistcategories`.
        '''
        url = 'https://api.kkbox.com/v1.1/featured-playlist-categories'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())

    @assert_access_token
    def fetch_feature_playlist_by_category(self, category_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches featured playlist by given category ID.

        :param category: the category.
        :type category: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs-en.kkbox.codes/v1.1/reference#featuredplaylistcategories-category_id`.
        '''
        url = 'https://api.kkbox.com/v1.1/featured-playlist-categories/%s' % category_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())        

    @assert_access_token
    def fetch_playlists_of_feature_playlist_category(self, category_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches playlists of featured playlist category by given ID.

        :param category: the category.
        :type category: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs-en.kkbox.codes/v1.1/reference#featuredplaylistcategories-category_id-playlists`.
        '''
        url = 'https://api.kkbox.com/v1.1/featured-playlist-categories/%s/playlists' % category_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())
