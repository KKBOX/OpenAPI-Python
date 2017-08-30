#!/usr/bin/env python
# encoding: utf-8

class KKBOXAccessToken:
    '''
    The access token object for accessing KKBOX's API.   
    '''
    def __init__(self, **kwargs):
        assert kwargs.get('access_token', None) != None
        #: The actual access token
        self.access_token = kwargs.get('access_token', None)
        #: The access token expiration date in unix timestamp
        self.expires_in = kwargs.get('expires_in', None)
        #: The token type
        self.token_type = kwargs.get('token_type', None)
        #: The scope of the token, may be none
        self.scope = kwargs.get('scope', None)
        #: The refresh token
        self.refresh_token = kwargs.get('refresh_token', None)
