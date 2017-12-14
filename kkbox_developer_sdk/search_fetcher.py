#!/usr/bin/env python
# encoding: utf-8
from .fetcher import *
from .territory import *

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
    Search API, the types it can search includes artists, albums, tracks, or playlists.
    Default to search all types, use "," to seperate types if you want to use multiple 
    types to search at the same time.

    See `https://kkbox.gelato.io/docs/versions/1.1/resources/search`.
    '''
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

        See `https://kkbox.gelato.io/docs/versions/1.1/resources/search/endpoints/get-search`.
        '''
        url = 'https://api.kkbox.com/v1.1/search'
        url += '?' + url_parse.urlencode({'q': keyword, 'territory': terr})
        if len(types) > 0:
            url += '&type=' + ','.join(types)
        return self.http._post_data(url, None, self.http._headers_with_access_token())
