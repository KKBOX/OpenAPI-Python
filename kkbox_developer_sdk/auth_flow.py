#!/usr/bin/env python
# encoding: utf-8
from .http import *
from .access_token import *

class KKBOXOAuth:
    '''
    Implements various KKBOX Oauth 2.0 authorization flows.

    See `https://docs-en.kkbox.codes/docs/appendix-b`.
    '''

    OAUTH_TOKEN_URL = 'https://account.kkbox.com/oauth2/token'

    def __init__(self, client_id, client_secret):
        #: The client ID
        self.client_id = client_id
        #: The client secret
        self.client_secret = client_secret
        #: The access token
        self.access_token = None
        #: The http client
        self.http = KKBOXHTTP()
        assert len(self.client_id) > 0, 'A client ID must be set.'
        assert len(self.client_secret) > 0, 'A client secret must be set.'

    def fetch_access_token_by_client_credentials(self):
        '''
        There are three ways to let you start using KKBOX's Open/Partner
        API. The first way among them is to generate a client
        credential to fetch an access token to let KKBOX identify
        you. It allows you to access public data from KKBOX such as
        public albums, playlists and so on.

        However, you cannot use client credentials to access private
        data of a user. You have to let users to log-in into KKBOX and
        grant permissions for you to do so. You cannot use client
        credentials to do media playback either, since it requires a
        Premium Membership.

        :return: an access token
        :rtype: :class:`kkbox_sdk.KKBOXAccessToken`

        See `https://docs-en.kkbox.codes/docs/appendix-a`.
        '''
        client_credential_base = '%s:%s' % (self.client_id, self.client_secret)
        try:
            client_credentials = base64.b64encode(
                bytes(client_credential_base, 'utf-8'))
        except:
            client_credentials = base64.b64encode(client_credential_base)
        client_credentials = client_credentials.decode('utf-8')
        headers = {'Authorization': 'Basic ' + client_credentials,
                   'Content-type': 'application/x-www-form-urlencoded'}
        post_parameters = {'grant_type': 'client_credentials',
                           'scope': 'user_profile user_territory'}
        json_object = self.http._post_data(KKBOXOAuth.OAUTH_TOKEN_URL, post_parameters,
                                      headers)
        self.access_token = KKBOXAccessToken(**json_object)
        return self.access_token





    

