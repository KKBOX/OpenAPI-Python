#!/usr/bin/env python
# encoding: utf-8

'''
SDK for KKBOX's Open/Partner API. https://docs.kkbox.codes
'''

from fetcher import *
from territory import *


class KKBOXSearchTypes:
    '''
    The Search types of the search API.
    '''
    ARTIST = 'artist'
    ALBUM = 'album'
    TRACK = 'track'
    PLAYLIST = 'playlist'

class KKBOXSearchFetcher(Fetcher):
    '''
    Search API.

    See `https://docs.kkbox.codes/docs/search`.
    '''
    @property
    def access_token(self):
        return self.http.access_token

    def __init__(self, access_token):
        self.http = KKBOXHTTP(access_token)

    @assert_access_token
    def search(self, keyword, types=[], terr=KKBOXTerritory.TAIWAN):
        '''
        Searches within KKBOX's database.

        :param keyword: the keyword.
        :type keyword: str
        :param types: the search types.
        :return: list
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/search`.
        '''
        url = 'https://api.kkbox.com/v1.1/search'
        url += '?' + url_parse.urlencode({'q': keyword, 'territory': terr})
        if len(types) > 0:
            url += '&type=' + ','.join(types)
        return self.http._post_data(url, None, self.http._headers_with_access_token())