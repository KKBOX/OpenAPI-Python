#!/usr/bin/env python
# encoding: utf-8

'''
SDK for KKBOX's Open/Partner API. https://docs.kkbox.codes
'''

from http import *
from access_token import *


class KKBOXDeviceCode:
    '''
    Get OAuth 2.0 Device code.
    '''

    def __init__(self, **kwargs):
        self.device_code = kwargs.get('device_code', None)
        self.short_verification_url = kwargs.get('short_verification_url', None)
        self.verification_url = kwargs.get('verification_url', None)
        self.verification_qrcode = kwargs.get('verification_qrcode', None)
        self.interval = kwargs.get('interval', None)
        self.expires_in = kwargs.get('expires_in', None)
        self.user_code = kwargs.get('user_code', None)

class KKBOXDeviceFlow:
    '''
    Implements the device flow. Used for devices that cannot enter username or 
    password easily like TV, game consoles.

    See `https://docs.kkbox.codes/docs/oauth-20-for-devices-flow`.
    '''
    OAUTH_TOKEN_URL = 'https://account.kkbox.com/oauth2/token'
    OAUTH_DEVICE_CODE_URL = 'https://account.kkbox.com/oauth2/device/code'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.http = KKBOXHTTP()
        assert len(self.client_id) > 0, 'A client ID must be set.'
        assert len(self.client_secret) > 0, 'A client secret must be set.'

    def fetch_device_code(self):
        '''
        If you are developing an app on devices such as an Android TV or an
        Apple TV, which do not have web views, or it is hard to let
        users to input log-in name or password on them, you may choose
        using Device Code.

        The Device Code mechanism shows a QR code image to users to let
        them scan the code using a PC or a smart phone, and then they
        will go to KKBOX's log-in page to complete logging-in and
        grant permissions for you. When it is done, he or she also
        completes logging-in on the device.

        Calling the method returns a KKBOXDeviceCode object. Please
        creates a QRCode image based on the 'verification_qrcod'
        member variable, and show it to users. In the mean while,
        please pass the value in the 'device_code' variable to the
        `fetch_access_token_by_device_code` method to try if it is
        able to obtain an access token repeatly, following the
        interval in the 'interval' variable, until users complete
        logging-in on their PCs and smart phones.

        :return: a device code.
        :rtype: :class:`kkbox_sdk.KKBOXDeviceCode`

        See `https://docs.kkbox.codes/docs/oauth-20-for-devices-flow` and
        `https://docs.kkbox.codes/docs/kkbox-oauth-20-device-code-api`.
        '''
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        post_parameters = {'scope': 'user_profile user_territory',
                           'client_id': self.client_id}
        json_object = self.http._post_data(KKBOXDeviceFlow.OAUTH_DEVICE_CODE_URL,
                                      post_parameters, headers)
        return KKBOXDeviceCode(**json_object)

    def fetch_access_token_by_device_code(self, device_code):
        '''
        The method helps to fetch access token by a Device Code. Please
        read about the method 'fetch_device_code' before calling it.

        :param device_code: the device code.
        :type device_code: str
        :return: an access token.
        :rtype: :class:`kkbox_sdk.KKBOXAccessToken`

        See `https://docs.kkbox.codes/docs/oauth-20-for-devices-flow` and
        `https://docs.kkbox.codes/docs/kkbox-oauth-20-device-code-api`.
        '''
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        post_parameters = {
            'grant_type': 'http://oauth.net/grant_type/device/1.0',
            'code': device_code,
            'client_id': self.client_id,
            'client_secret': self.client_secret}
        json_object = self.http._post_data(KKBOXDeviceFlow.OAUTH_TOKEN_URL, post_parameters,
                                      headers)
        self.access_token = KKBOXAccessToken(**json_object)
        return self.access_token

