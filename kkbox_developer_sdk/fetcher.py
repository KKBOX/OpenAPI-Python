#!/usr/bin/env python
# encoding: utf-8

from .http import *

def assert_access_token(func, *args):
        @functools.wraps(func)
        def _inner(*args, **kwargs):
            self = args[0]
            assert self.access_token != None, 'An access token is requires.'
            assert len(
                self.access_token.access_token) > 0, 'An access token is requires.'
            return func(*args, **kwargs)
        return _inner


class Fetcher:
    '''
    Base class for various fetchers.
    '''
    @property
    def access_token(self):
        return self.http.access_token

    def __init__(self, access_token):
        #: The http client
        self.http = KKBOXHTTP(access_token)
    
    def fetch_next_page(self, data):
        '''
        Fetches next page based on previously fetched data.
        Will get the next page url from data['paging']['next'].

        :param data: previously fetched API response.
        :type data: dict        
        :return: API response.
        :rtype: dict
        '''
        next_url = data['paging']['next']
        if next_url != None:
            next_data = self.http._post_data(next_url, None, self.http._headers_with_access_token())
            return next_data
        else:
            return None

    def fetch_data(self, url):
        ''' 
        Fetches data from specific url.

        :return: The response.
        :rtype: dict
        '''
        return self.http._post_data(url, None, self.http._headers_with_access_token())

