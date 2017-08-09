#!/usr/bin/env python
# encoding: utf-8

import sys

sys.path.append('../')
from kkbox_sdk import *
from authTest import *


class TestAPISDK(unittest.TestCase):
	
    def _validate_image(self, image):
        keys = ('url', 'width', 'height')
        for key in keys:
            assert key in image, 'missing key ' + key        

    '''
    def _validate_paging(self, paging):
        keys = ('offset', 'limit', 'previous', 'next')
        for key in keys:
            assert key in paging, 'missing key ' + key
    '''

    def _validate_artist(self, artist):
        keys = ('id', 'name', 'url', 'images')
        for key in keys:
            assert key in artist, 'missing key ' + key
        for image in artist['images']:
            self._validate_image(image)

    def _validate_album(self, album):
        keys = ('id', 'name', 'url', 'explicitness', 'available_territories', 'images')
        for key in keys:
            assert key in album, 'missing key ' + key
        for image in album['images']:
            self._validate_image(image)
        if 'artist' in album:
            self._validate_artist(album['artist'])

    def _validate_track(self, track):
        keys = ('id', 'name', 'url', 'track_number', 'explicitness', 'available_territories')
        for key in keys:
            assert key in track, 'missing key ' + key
        if 'album' in track:
            self._validate_album(track['album'])
        if 'paging' in track:
            assert 'offset', 'limit' in track['paging']
            assert 'previous', 'next' in track['paging']

    def _validate_playlist(self, playlist):
        keys = ('id', 'title', 'description', 'url', 'images', 'owner')
        for key in keys:
            assert key in playlist, 'missing key ' + key
        for image in playlist['images']:
            self._validate_image(image)
        for owner in playlist['owner']:
            assert 'id', 'name' in playlist['owner']
        if 'tracks' in playlist:
            for track in playlist['tracks']['data']:
                self._validate_track(track)
        if 'paging' in playlist:
            assert 'offset', 'limit' in playlist['paging']
            assert 'previous', 'next' in playlist['paging']

    def test_fetch_track(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        track_id = '4kxvr3wPWkaL9_y3o_'
        track = sdk.fetch_track(track_id)
        self._validate_track(track)

    def test_fetch_artist(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        artist_id = '8q3_xzjl89Yakn_7GB'
        artist = sdk.fetch_artist(artist_id)
        self._validate_artist(artist)

    def test_fetch_albums_of_artist(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        artist_id = 'CluDKLYxr1GFQqLSZt'
        albums = sdk.fetch_albums_of_artist(artist_id)
        for album in albums['data']:
            self._validate_album(album)

    def test_fetch_top_tracks_of_artist(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        artist_id = 'CluDKLYxr1GFQqLSZt'
        tracks = sdk.fetch_top_tracks_of_artist(artist_id)
        for track in tracks['data']:
            self._validate_track(track)

    def test_fetch_album(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        album_id = 'WpTPGzNLeutVFHcFq6'
        album = sdk.fetch_album(album_id)
        self._validate_album(album)

    def test_fetch_tracks_in_album(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        album_id = 'WpTPGzNLeutVFHcFq6'
        tracks = sdk.fetch_tracks_in_album(album_id)
        for track in tracks['data']:
            self._validate_track(track)
    
    def test_fetch_shared_playlist(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        playlist_id = '4nUZM-TY2aVxZ2xaA-'
        playlist = sdk.fetch_shared_playlist(playlist_id)
        self._validate_playlist(playlist)
    
    def test_fetch_tracks_of_shared_playlist(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        playlist_id = '4nUZM-TY2aVxZ2xaA-'
        playlist = sdk.fetch_tracks_of_shared_playlists(playlist_id)
        for track in playlist['data']:
            self._validate_track(track)        

    def test_search(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        results = sdk.search('BTS',
                             [KKBOXSearchTypes.ARTIST, KKBOXSearchTypes.ALBUM,
                              KKBOXSearchTypes.TRACK,
                              KKBOXSearchTypes.PLAYLIST])
        artists = results.get('artists', [])
        for artist in artists['data']:
            self._validate_artist(artist)
        albums = results.get('albums', [])
        for album in albums['data']:
            self._validate_album(album)
        tracks = results.get('tracks', [])
        for track in tracks['data']:
            self._validate_track(track)
        playlists = results.get('playlists', [])
        for playlist in playlists['data']:
            self._validate_playlist(playlist)

    def test_fetch_charts(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        charts = sdk.fetch_charts()
        keys = ('paging', 'data', 'summary')
        for key in keys:
            assert key in charts, 'missing key ' + key
        for chart in charts['data']:
            self._validate_playlist(chart)
        for paging in charts['paging']:
            assert 'offset', 'limit' in charts['paging']
            assert 'previous', 'next' in charts['paging']

    def test_fetch_new_release_categories(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        categories = sdk.fetch_new_release_categories()
        keys = ('paging', 'data', 'summary')
        for key in keys:
            assert key in categories, 'missing key ' + key
        for category in categories['data']:
            keys = ('id', 'title')
            for key in keys:
                assert key in category
        for paging in categories['paging']:
            assert 'offset', 'limit' in categories['paging']
            assert 'previous', 'next' in categories['paging']

    def test_fetch_new_release_category(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        category_id = '1ZQwmFTaLE4p7BG-Ua'
        category = sdk.fetch_new_release_category(category_id)
        keys = ('id', 'title', 'albums')
        for key in keys:
            assert key in category, 'missing key ' + key
        for album in category['albums']['data']:
            self._validate_album(album)

    def test_fetch_albums_of_new_release_category(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        category_id = '1ZQwmFTaLE4p7BG-Ua'
        albums = sdk.fetch_albums_of_new_release_category(category_id)
        for album in albums['data']:
            self._validate_album(album)

    def test_fetch_all_genre_stations(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        stations = sdk.fetch_all_genre_stations()
        keys = ('paging', 'data', 'summary')
        for key in keys:
            assert key in stations, 'missing key ' + key
        for station in stations['data']:
            keys = ('category', 'id', 'name')
            for key in keys:
                assert key in station
        for paging in stations['paging']:
            assert 'offset', 'limit' in stations['paging']
            assert 'previous', 'next' in stations['paging']

    def test_fetch_genre_station(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        station_id = 'TYq3EHFTl-1EOvJM5Y'
        station = sdk.fetch_genre_station(station_id)
        keys = ('category', 'tracks', 'id', 'name')
        for key in keys:
            assert key in station
        tracks = station['tracks']['data']
        for track in tracks:
            self._validate_track(track)

    def test_fetch_all_mood_stations(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        stations = sdk.fetch_all_mood_stations()
        keys = ('paging', 'data', 'summary')
        for key in keys:
            assert key in stations, 'missing key ' + key
        for station in stations['data']:
            keys = ('images', 'id', 'name')
            for key in keys:
                assert key in station, 'missing key ' + key
            for image in station['images']:
                self._validate_image(image)
        for paging in stations['paging']:
            assert 'offset', 'limit' in stations['paging']
            assert 'previous', 'next' in stations['paging']

    def test_fetch_mood_station(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        station_id = 'StGZp2ToWq92diPHS7'
        station = sdk.fetch_mood_station(station_id)
        keys = ('tracks', 'id', 'name')
        for key in keys:
            assert key in station
        tracks = station['tracks']['data']
        for track in tracks:
            self._validate_track(track)

            # def test_fetch_media_provision(self):
            #   sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
            #   # url = sdk.generate_url_for_getting_auth_code('http://example.com', 1234)
            #   # print url
            #   code = 'ba91244b3a8d2556bbf0f1a7350373be'
            #   sdk.fetch_access_token_by_auth_code(code)
            #   print sdk.access_token.access_token
            #   track_id = '4kxvr3wPWkaL9_y3o_'
            #   media_provision = sdk.fetch_media_provision(track_id)
            #   print media_provision

    def test_fetch_feature_playlists(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        feature_playlists = sdk.fetch_feature_playlists()
        keys = ('paging', 'data', 'summary')
        for key in keys:
            assert key in feature_playlists, 'missing key ' + key
        for playlist in feature_playlists['data']:
            keys = ('id', 'title', 'description', 'url', 'images')
            for key in keys:
                assert key in playlist, 'missing key ' + key
            for image in playlist['images']:
                self._validate_image(image)
        for paging in feature_playlists['paging']:
            assert 'offset', 'limit' in feature_playlists['paging']
            assert 'previous', 'next' in feature_playlists['paging']

    def test_fetch_categories_of_feature_playlist(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        categories = sdk.fetch_categories_of_feature_playlist()
        keys = ('paging', 'data', 'summary')
        for key in keys:
            assert key in categories, 'missing key ' + key
        for category in categories['data']:
            keys = ('id', 'title', 'images')
            for key in keys:
                assert key in category, 'missing key ' + key
            for image in category['images']:
                self._validate_image(image)
        for paging in categories['paging']:
            assert 'offset', 'limit' in categories['paging']
            assert 'previous', 'next' in categories['paging']

    def test_fetch_feature_playlist_by_category(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        category_id = '9XQKD8BJx595ESs_rb'
        category = sdk.fetch_feature_playlist_by_category(category_id)
        keys = ('id', 'title', 'images', 'playlists')
        for key in keys:
            assert key in category, 'missing key ' + key
        for image in category['images']:
            self._validate_image(image)
        for playlist in category['playlists']['data']:
            self._validate_playlist(playlist)

    def test_fetch_playlists_of_feature_playlist_category(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        category_id = '9XQKD8BJx595ESs_rb'
        category = sdk.fetch_playlists_of_feature_playlist_category(category_id)
        keys = ('paging', 'data', 'summary')
        for key in keys:
            assert key in category, 'missing key ' + key
        for playlist in category['data']:
            self._validate_playlist(playlist)
        for paging in category['paging']:
            assert 'offset', 'limit' in category['paging']
            assert 'previous', 'next' in category['paging']

    def test_fetch_all_new_hits_playlists(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        new_hits = sdk.fetch_all_new_hits_playlists()
        keys = ('paging', 'data', 'summary')
        for key in keys:
            assert key in new_hits, 'missing key ' + key
        for playlist in new_hits['data']:
            self._validate_playlist(playlist)
        for paging in new_hits['paging']:
            assert 'offset', 'limit' in new_hits['paging']
            assert 'previous', 'next' in new_hits['paging']

    def test_fetch_new_hits_playlist(self):
        sdk = KKBOXSDK(CLIENT_ID, CLIENT_SECRET)
        sdk.fetch_access_token_by_client_credentials()
        playlist_id = 'DZrC8m29ciOFY2JAm3'
        new_hits = sdk.fetch_new_hits_playlist(playlist_id)
        self._validate_playlist(new_hits)


if __name__ == '__main__':
    unittest.main()