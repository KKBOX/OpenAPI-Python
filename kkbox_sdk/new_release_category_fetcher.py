#!/usr/bin/env python
# encoding: utf-8

'''
SDK for KKBOX's Open/Partner API. https://docs.kkbox.codes
'''

from fetcher import *
from territory import *


class KKBOXNewReleaseCategoryFetcher(Fetcher):
    '''
    List categories of new release albums.

    See `https://docs.kkbox.codes/docs/new-release-categories`.
    '''
    @property
    def access_token(self):
        return self.http.access_token

    def __init__(self, access_token):
        self.http = KKBOXHTTP(access_token)

    @assert_access_token
    def fetch_all_new_release_categories(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches new release categories.

        :param terr: the current territory.
        :return: API response.
        :rtype: list

        See `https://docs.kkbox.codes/docs/new-release-categories`
        '''
        url = 'https://api.kkbox.com/v1.1/new-release-categories'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())

    @assert_access_token
    def fetch_new_release_category(self, category_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches new release categories by given ID.

        :param category_id: the station ID.
        :type category_id: str
        :param terr: the current territory.
        :return: API response.
        :rtype: list

        See `https://docs.kkbox.codes/docs/new-release-categories-category-id`
        '''
        url = 'https://api.kkbox.com/v1.1/new-release-categories/%s' % category_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())

    @assert_access_token
    def fetch_albums_of_new_release_category(self, category_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches albums of new release category by given ID.

        :param category_id: the category ID.
        :type category_id: str
        :param terr: the current territory.
        :return: API response.
        :rtype: list

        See `https://docs.kkbox.codes/docs/new-release-categories-category-id-albums`
        '''
        url = 'https://api.kkbox.com/v1.1/new-release-categories/%s/albums' % category_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self.http._post_data(url, None, self.http._headers_with_access_token())