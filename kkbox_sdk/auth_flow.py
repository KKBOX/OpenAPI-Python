#!/usr/bin/env python
# encoding: utf-8

'''
SDK for KKBOX's Open/Partner API. https://docs.kkbox.codes
'''

from http import *
from access_token import *


class KKBOXOAuth:
    '''
    Implements various KKBOX Oauth 2.0 authorization flows.

    See `https://docs.kkbox.codes/docs/authorization-code-flow`.
    '''

    OAUTH_TOKEN_URL = 'https://account.kkbox.com/oauth2/token'
    OAUTH_AUTH_URL = 'https://account.kkbox.com/oauth2/authorize'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
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

        See `https://docs.kkbox.codes/docs/client-credentials-flow` and
        `https://docs.kkbox.codes/docs/kkbox-oauth-20-token-api`.
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

    def generate_url_for_getting_auth_code(self, callback_url, state):
        '''
        There are three ways to let you start using KKBOX's Open/Partner
        API. If you are developing a web site, a mobile app or a
        native desktop app, the Authorization Code mechanism is what
        you are looking for.

        At first, you need to open KKBOX's log-in page to let users to
        do logging-in, and then let them grant permissions for
        you. You will be a get parameter named 'code' in your callback
        URL. If you are doing a mobile or desktop app, a web view is
        required, and you can set your custom callback URL as well.

        To use the returned Authorization Code, pass it to the next
        method 'fetch_access_token_by_auth_code', you will get an
        access token.

        :param callback_url: the callback URL.
        :type callback_url: str
        :return: URL for user to do logging-in.
        :rtype: str

        See `https://docs.kkbox.codes/docs/authorization-code-flow` and
        `https://docs.kkbox.codes/docs/kkbox-oauth-20-authorize-api`.
        '''
        get_parameters = {'client_id': self.client_id,
                          'redirect_uri': callback_url,
                          'scope': 'user_profile user_territory',
                          'state': state,
                          'response_type': 'code'
                          }
        url =  KKBOXOAuth.OAUTH_AUTH_URL + '?' + url_parse.urlencode(get_parameters)
        return url


    def fetch_access_token_by_auth_code(self, auth_code):
        '''
        The method helps to fetch an access token by using a Authorization
        Code. To obtain an Authorization Code, please read the
        documentation about the 'generate_url_for_getting_auth_code' method.

        :param auth_code: the auth code.
        :type auth_code: str
        :return: an access token.
        :rtype: :class:`kkbox_sdk.KKBOXAccessToken`

        See `https://docs.kkbox.codes/docs/authorization-code-flow` and
        `https://docs.kkbox.codes/docs/kkbox-oauth-20-authorize-api`.
        '''
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        post_parameters = {'grant_type': 'authorization_code',
                           'scope': 'user_profile user_territory',
                           'code': auth_code,
                           'client_id': self.client_id,
                           'client_secret': self.client_secret}
        json_object = self.http._post_data(KKBOXOAuth.OAUTH_TOKEN_URL, post_parameters,
                                      headers)
        self.access_token = KKBOXAccessToken(**json_object)
        return self.access_token

    

