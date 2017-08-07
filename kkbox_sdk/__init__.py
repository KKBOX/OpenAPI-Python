#!/usr/bin/env python
# encoding: utf-8

'''
SDK for KKBOX's Open/Partner API. https://docs.kkbox.codes
'''

try:
    # Python 3
    import urllib.parse as url_parse
    import urllib.request as url_request
except:
    # Python 2
    import urllib as url_parse
    import urllib2 as url_request
    import functools
import base64
import json

import unittest

def assert_access_token(func, *args):
    @functools.wraps(func)
    def _inner(*args, **kwargs):
        self = args[0]
        assert self.access_token != None, 'An access token is requires.'
        assert len(
            self.access_token.access_token) > 0, 'An access token is requires.'
        return func(*args, **kwargs)

    return _inner


class KKBOXAccessToken:
    '''
    The access token object for accessing KKBOX's API.
    '''

    def __init__(self, **kwargs):
        assert kwargs.get('access_token', None) != None
        self.access_token = kwargs.get('access_token', None)
        self.expires_in = kwargs.get('expires_in', None)
        self.token_type = kwargs.get('token_type', None)
        self.scope = kwargs.get('scope', None)


class KKBOXDeviceCode:
    def __init__(self, **kwargs):
        self.device_code = kwargs.get('device_code', None)
        self.short_verification_url = kwargs.get('short_verification_url', None)
        self.verification_url = kwargs.get('verification_url', None)
        self.verification_qrcode = kwargs.get('verification_qrcode', None)
        self.interval = kwargs.get('interval', None)
        self.expires_in = kwargs.get('expires_in', None)
        self.user_code = kwargs.get('user_code', None)


class KKBOXTerritory:
    TAIWAN = 'TW'
    HONGKONG = 'HK'
    SINGAPORE = 'SG'
    MALAYSIA = 'MA'
    JAPAN = 'JP'
    THAILAND = 'TH'


class KKBOXSearchTypes:
    ARTIST = 'artist'
    ALBUM = 'album'
    TRACK = 'track'
    PLAYLIST = 'playlist'


class KKBOXChartPeriod:
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'


class KKBOXSDK:
    OAUTH_TOKEN_URL = 'https://account.kkbox.com/oauth2/token'
    OAUTH_AUTH_URL = 'https://account.kkbox.com/oauth2/authorize'
    OAUTH_DEVICE_CODE_URL = 'https://account.kkbox.com/oauth2/device/code'
    USER_AGENT = 'KKBOX Open/Partner API Python SDK'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        assert len(self.client_id) > 0, 'A client ID must be set.'
        assert len(self.client_secret) > 0, 'A client secret must be set.'

    def _do_post(self, url, data, headers):
        try:  # Python 3
            if data != None:
                data = bytes(data, 'utf-8')
        except:  # Python 2
            pass

        try:
            req = url_request.Request(url=url, data=data, headers=headers)
            req.add_header('User-Agent', KKBOXSDK.USER_AGENT)
            f = url_request.urlopen(req)
            r = f.read()
        except url_request.HTTPError as e:
            print(e.fp.read())
            raise (e)
        except Exception  as e:
            raise (e)

        try:  # Python 3
            r = str(r, 'utf-8')
        except:  # Python 2
            pass
        json_object = json.loads(r)
        return json_object

    def _post_data(self, url, post_parameters, headers):
        data = url_parse.urlencode(
            post_parameters) if post_parameters != None else None
        return self._do_post(url, data, headers)

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
        json_object = self._post_data(KKBOXSDK.OAUTH_TOKEN_URL, post_parameters,
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
        url =  KKBOXSDK.OAUTH_AUTH_URL + '?' + url_parse.urlencode(get_parameters)
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
        json_object = self._post_data(KKBOXSDK.OAUTH_TOKEN_URL, post_parameters,
                                      headers)
        self.access_token = KKBOXAccessToken(**json_object)
        return self.access_token

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
        json_object = self._post_data(KKBOXSDK.OAUTH_DEVICE_CODE_URL,
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
        json_object = self._post_data(KKBOXSDK.OAUTH_TOKEN_URL, post_parameters,
                                      headers)
        self.access_token = KKBOXAccessToken(**json_object)
        return self.access_token

    def _headers_with_access_token(self):
        return {'Authorization': 'Bearer %s' % self.access_token.access_token}

    @assert_access_token
    def fetch_track(self, track_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches a song track by given ID.

        :param track_id: the track ID.
        :type track_id: str
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/tracks`.
        '''
        url = 'https://api.kkbox.com/v1.1/tracks/%s' % track_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_artist(self, artist_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches an artist by given ID.

        :param artist_id: the artist ID.
        :type artist_id: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/artists`.
        '''
        url = 'https://api.kkbox.com/v1.1/artists/%s' % artist_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_albums_of_artist(self, artist_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches albums belong to an artist by given ID.

        :param artist_id: the artist ID.
        :type artist_id: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/artists-albums`.
        '''
        url = 'https://api.kkbox.com/v1.1/artists/%s/albums' % artist_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())
    
    @assert_access_token
    def fetch_top_tracks_of_artist(self, artist_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetcher top tracks belong to an artist by given ID.

        :param artist_id: the artist ID.
        :type artist_id: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See 'https://docs.kkbox.codes/docs/artists-top-tracks'
        '''
        url = 'https://api.kkbox.com/v1.1/artists/%s/top-tracks' % artist_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_album(self, album_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches an album by given ID.

        :param album_id: the album ID.
        :type album_id: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/albums`.
        '''
        url = 'https://api.kkbox.com/v1.1/albums/%s' % album_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_tracks_in_album(self, album_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches tracks in an album by given ID.

        :param album_id: the album ID.
        :type album_id: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/albums-tracks`.
        '''
        url = 'https://api.kkbox.com/v1.1/albums/%s/tracks' % album_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())   
    
    @assert_access_token
    def fetch_shared_playlist(self, playlist_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches a shared playlist by given ID.

        :param playlist_id: the playlist ID.
        :type playlist_id: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dictcd

        See `https://docs.kkbox.codes/docs/shared-playlists`.
        '''
        url = 'https://api.kkbox.com/v1.1/shared-playlists/%s' % playlist_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())
    
    @assert_access_token
    def fetch_tracks_of_shared_playlists(self, playlist_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches track list of a playlist by given ID.

        :param playlist_id: the playlist ID.
        :type playlist_id: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/shared-playlistsplaylist_idtrackss`.
        '''
        url = 'https://api.kkbox.com/v1.1/shared-playlists/%s/tracks' % playlist_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

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
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_charts(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches chart categories.

        :param terr: the current territory.
        :return: API response.
        :rtype: list

        See `https://docs.kkbox.codes/docs/charts`
        '''
        url = 'https://api.kkbox.com/v1.1/charts'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_new_release_categories(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches new release categories.

        :param terr: the current territory.
        :return: API response.
        :rtype: list

        See `https://docs.kkbox.codes/docs/new-release-categories`
        '''
        url = 'https://api.kkbox.com/v1.1/new-release-categories'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

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
        return self._post_data(url, None, self._headers_with_access_token())

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
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_all_genre_stations(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches all genre stations.

        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/genre-stations-genre`.
        '''
        url = 'https://api.kkbox.com/v1.1/genre-stations'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_genre_station(self, station_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches a genre station by given ID.

        :param station_id: the station ID
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/genre-stations-station`.
        '''
        url = 'https://api.kkbox.com/v1.1/genre-stations/%s' % station_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_all_mood_stations(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches all mood stations.

        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/mood-stations-mood`.
        '''
        url = 'https://api.kkbox.com/v1.1/mood-stations'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_mood_station(self, station_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches a mood station by given ID.

        :param station_id: the station ID
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/mood-stations-station`.
        '''
        url = 'https://api.kkbox.com/v1.1/mood-stations/%s' % station_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_feature_playlists(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches featured playlists.

        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/featured-playlists`.
        '''
        url = 'https://api.kkbox.com/v1.1/featured-playlists'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_categories_of_feature_playlist(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches categories of featured playlist.

        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/featured-playlist-categories`.
        '''
        url = 'https://api.kkbox.com/v1.1/featured-playlist-categories'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_feature_playlist_by_category(self, category_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches featured playlist by given category ID.

        :param category: the category.
        :type category: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/feature-playlist-category`.
        '''
        url = 'https://api.kkbox.com/v1.1/featured-playlist-categories/%s' % category_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())        

    @assert_access_token
    def fetch_playlists_of_feature_playlist_category(self, category, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches playlist of featured playlist category by given ID.

        :param category: the category.
        :type category: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/featured-playlist-categoriescategoriesplaylists`.
        '''
        url = 'https://api.kkbox.com/v1.1/featured-playlist-categories/%s/playlists' % category
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_all_new_hits_playlists(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches all new hits playlists.

        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See 'https://docs.kkbox.codes/docs/new-hits-playlists'
        '''
        url = 'https://api.kkbox.com/v1.1/new-hits-playlists'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_new_hits_playlist(self, playlist_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches new hits playlist by given ID.

        :param playlist_id: the category.
        :type playlist_id: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See 'https://docs.kkbox.codes/docs/new-hits-playlists-playlist-id'
        '''
        url = 'https://api.kkbox.com/v1.1/new-hits-playlists/%s' % playlist_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_user_profile(self, user_id):
        '''
        Fetches profile of a user by given ID.

        :param user_id: the user ID.
        :type user_id: str
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/user-profile`.
        '''
        url = 'https://api.kkbox.com/v1.1/users/%s' % user_id
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_user_shared_playlists(self, user_id):
        '''
        Fetches playlists of a user by given ID.

        :param user_id: the user ID.
        :type user_id: str
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/user-shared-playlist`.
        '''
        url = 'https://api.kkbox.com/v1.1/users/%s/shared-playlists' % user_id
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_user_album_collection(self, user_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches album collection of a user by given ID.

        :param user_id: the user ID.
        :type user_id: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/users-album-collection`.
        '''
        url = 'https://api.kkbox.com/v1.1/users/%s/album-collection' % user_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_user_playlist_collection(self, user_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches playlist collection of a user by given ID.

        :param user_id: the user ID.
        :type user_id: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/users-playlist-collection`.
        '''
        url = 'https://api.kkbox.com/v1.1/users/%s/playlist-collection' % user_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_my_profile(self):
        '''
        Fetches profile of current user.

        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/me`.
        '''
        url = 'https://api.kkbox.com/v1.1/me'
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_my_shared_playlists(self):
        '''
        Fetches shared playlists of current user.

        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/me-shared-playlists`.
        '''
        url = 'https://api.kkbox.com/v1.1/me/shared-playlists'
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_my_favorite(self):
        '''
        Fetches favorite tracks of current user.

        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/me-favorite-tracks`.
        '''
        url = 'https://api.kkbox.com/v1.1/me/favorite'
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_my_playlists(self):
        '''
        Fetches playlists of current user.

        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/me-playlists`.
        '''
        url = 'https://api.kkbox.com/v1.1/me/playlists'
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_my_album_collection(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches album collection of current user.

        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/me-album-collection`.
        '''
        url = 'https://api.kkbox.com/v1.1/me/album-collection'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_my_playlist_collection(self, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches playlist collection of current user.

        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/me-playlist-collection`.
        '''
        url = 'https://api.kkbox.com/v1.1/me/playlist-collection'
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_my_private_playlist(self, private_playlist_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches private playlists of current user by given ID.

        :param private_playlist_id: the private playlist ID.
        :type artist_id: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/me-playlist-id`.
        '''
        url = 'https://api.kkbox.com/v1.1/me/playlists/%s' % private_playlist_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_tracks_of_my_private_playlist(self, private_playlist_id, terr=KKBOXTerritory.TAIWAN):
        '''
        Fetches private playlists tracks of current user by given ID.

        :param private_playlist_id: the private playlist ID.
        :type artist_id: str
        :param terr: the current territory.
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/meplaylistsprivate_playlist_idtracks`.
        '''
        url = 'https://api.kkbox.com/v1.1/me/playlists/%s/tracks' % private_playlist_id
        url += '?' + url_parse.urlencode({'territory': terr})
        return self._post_data(url, None, self._headers_with_access_token())

    @assert_access_token
    def fetch_media_provision(self, track_id):
        '''
        Fetches a media provision, as known as "tickets".
        :param track_id: the track ID
        :type track_id: str
        :return: API response.
        :rtype: dict

        See `https://docs.kkbox.codes/docs/tickets`.
        '''
        headers = {
            'Authorization': 'Bearer %s' % self.access_token.access_token,
            'Content-Type': 'application/json'}
        url = 'https://api.kkbox.com/v1.1/tickets'
        return self._do_post(url, json.dumps({'track_id': track_id}), headers)
