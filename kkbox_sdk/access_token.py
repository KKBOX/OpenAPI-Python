#!/usr/bin/env python
# encoding: utf-8

class KKBOXAccessToken:

    # The access token object for accessing KKBOX's API.   

    def __init__(self, **kwargs):
        assert kwargs.get('access_token', None) != None
        self.access_token = kwargs.get('access_token', None)
        self.expires_in = kwargs.get('expires_in', None)
        self.token_type = kwargs.get('token_type', None)
        self.scope = kwargs.get('scope', None)
