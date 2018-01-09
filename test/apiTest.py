#!/usr/bin/env python
# encoding: utf-8

import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from kkbox_developer_sdk.track_fetcher import *
from kkbox_developer_sdk.artist_fetcher import *
from kkbox_developer_sdk.album_fetcher import *
from kkbox_developer_sdk.shared_playlist_fetcher import *
from kkbox_developer_sdk.search_fetcher import *
from kkbox_developer_sdk.chart_fetcher import *
from kkbox_developer_sdk.new_release_category_fetcher import *
from kkbox_developer_sdk.genre_station_fetcher import *
from kkbox_developer_sdk.mood_station_fetcher import *
from kkbox_developer_sdk.feature_playlist_fetcher import *
from kkbox_developer_sdk.feature_playlist_category_fetcher import *
from kkbox_developer_sdk.new_hits_playlist_fetcher import *
from kkbox_developer_sdk.auth_flow import *
from client import ClientInfo

CLIENT_ID = ClientInfo.client_id
CLIENT_SECRET = ClientInfo.client_secret

class TestAPISDK(unittest.TestCase):
	
    def _validate_image(self, image):
        keys = ('url', 'width', 'height')
        for key in keys:
            assert key in image, 'missing key ' + key        

    def _validate_paging(self, paging):
        assert 'offset', 'limit' in paging
        assert 'previous', 'next' in paging

    def _validate_artist(self, artist):
        keys = ('id', 'name', 'url', 'images')
        for key in keys:
            assert key in artist, 'missing key ' + key
        for image in artist['images']:
            self._validate_image(image)

    def _validate_artist_paging(self, artist_paging):
        if artist_paging is None:
            pass
        else:
            keys = ('paging', 'data', 'summary')
            for key in keys:
                assert key in artist_paging, 'missing key ' + key
            for artist in artist_paging['data']:
                self._validate_artist(artist)
            for paging in artist_paging['paging']:
                self._validate_paging(paging)

    def _validate_album(self, album):
        keys = ('id', 'name', 'url', 'explicitness', 'available_territories', 'images')
        for key in keys:
            assert key in album, 'missing key ' + key
        for image in album['images']:
            self._validate_image(image)
        if 'artist' in album:
            self._validate_artist(album['artist'])

    def _validate_album_paging(self, album_paging):
        if album_paging is None:
            pass
        else:
            keys = ('paging', 'data', 'summary')
            for key in keys:
                assert key in album_paging, 'missing key ' + key
            for album in album_paging['data']:
                self._validate_album(album)
            for paging in album_paging['paging']:
                self._validate_paging(paging)

    def _validate_track(self, track):
        keys = ('id', 'name', 'url', 'track_number', 'explicitness', 'available_territories')
        for key in keys:
            assert key in track, 'missing key ' + key
        if 'album' in track:
            self._validate_album(track['album'])
        if 'paging' in track:
            self._validate_paging(track['paging'])

    def _validate_track_paging(self, track_paging):
        if track_paging is None:
            pass
        else:
            keys = ('paging', 'data', 'summary')
            for key in keys:
                assert key in track_paging, 'missing key ' + key
            for track in track_paging['data']:
                self._validate_track(track)
            for paging in track_paging['paging']:
                self._validate_paging(paging)

    def _validate_playlist(self, playlist):
        if playlist is None:
            pass
        else:
            keys = ('id', 'title', 'description', 'url', 'images', 'owner')
            for key in keys:
                assert key in playlist, 'missing key ' + key
            for image in playlist['images']:
                self._validate_image(image)
            for owner in playlist['owner']:
                assert 'id', 'name' in playlist['owner']
            if 'tracks' in playlist:
                track = playlist['tracks']
                self._validate_track_paging(track)
            if 'paging' in playlist:
                self._validate_paging(playlist['paging'])

    def _validate_playlist_paging(self, playlist_paging):
        if playlist_paging is None:
            pass
        else:
            keys = ('paging', 'data', 'summary')
            for key in keys:
                assert key in playlist_paging, 'missing key ' + key
            for playlist in playlist_paging['data']:
                self._validate_playlist(playlist)
            for paging in playlist_paging['paging']:
                self._validate_paging(playlist_paging['paging'])

    def _validate_category(self, category):
        if category is None:
            pass
        else:
            keys = ('id', 'title')
            for key in keys:
                assert key in category, 'missing key ' + key
            if 'albums' in category:
                album = category['albums']
                self._validate_album_paging(album)
            if 'images' in category:
                for image in category['images']:
                    self._validate_image(image)

    def _validate_category_paging(self, category_paging):
        if category_paging is None:
            pass
        else:
            keys = ('paging', 'data', 'summary')
            for key in keys:
                assert key in category_paging, 'missing key ' + key
            for category in category_paging['data']:
                self._validate_category(category)
            for paging in category_paging['paging']:
                self._validate_paging(paging)

    def _validate_genre_station_paging(self, station_paging):
        if station_paging is None:
            pass
        else:
            keys = ('paging', 'data', 'summary')
            for key in keys: 
                assert key in station_paging, 'missing key ' + key
            for station in station_paging['data']:
                keys = ('category', 'id', 'name')
                for key in keys:
                    assert key in station
            for paging in station_paging['paging']:
                self._validate_paging(paging)

    def _validate_mood_station_paging(self, station_paging):
        if station_paging is None:
            pass
        else:
            keys = ('paging', 'data', 'summary')
            for key in keys: 
                assert key in station_paging, 'missing key ' + key
            for station in station_paging['data']:
                keys = ('images', 'id', 'name')
                for key in keys:
                    assert key in station
                for image in station['images']:
                    self._validate_image(image)
            for paging in station_paging['paging']:
                self._validate_paging(paging)

    def test_fetch_track(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXTrackFetcher(token)
        track_id = '4kxvr3wPWkaL9_y3o_'
        track = fetcher.fetch_track(track_id)
        self._validate_track(track)

    def test_fetch_artist(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXArtistFetcher(token)
        artist_id = '8q3_xzjl89Yakn_7GB'
        artist = fetcher.fetch_artist(artist_id)
        self._validate_artist(artist)

    def test_fetch_albums_of_artist(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXArtistFetcher(token)
        artist_id = 'CluDKLYxr1GFQqLSZt'
        albums = fetcher.fetch_albums_of_artist(artist_id)
        self._validate_album_paging(albums)
        next_page_data = fetcher.fetch_next_page(albums)
        self._validate_album_paging(next_page_data)

    def test_fetch_top_tracks_of_artist(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXArtistFetcher(token)
        artist_id = 'CluDKLYxr1GFQqLSZt'
        tracks = fetcher.fetch_top_tracks_of_artist(artist_id)
        self._validate_track_paging(tracks)
        next_page_data = fetcher.fetch_next_page(tracks)
        self._validate_track_paging(next_page_data)

    def test_fetch_related_artists(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXArtistFetcher(token)
        artist_id = 'CluDKLYxr1GFQqLSZt'
        artists = fetcher.fetch_related_artists(artist_id)
        self._validate_artist_paging(artists)
        next_page_data = fetcher.fetch_next_page(artists)
        self._validate_artist_paging(next_page_data)


    def test_fetch_album(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXAlbumFetcher(token)
        album_id = 'WpTPGzNLeutVFHcFq6'
        album = fetcher.fetch_album(album_id)
        self._validate_album(album)

    def test_fetch_tracks_in_album(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXAlbumFetcher(token)
        album_id = 'WpTPGzNLeutVFHcFq6'
        tracks = fetcher.fetch_tracks_in_album(album_id)
        self._validate_track_paging(tracks)
        next_page_data = fetcher.fetch_next_page(tracks)
        self._validate_track_paging(next_page_data)

    def test_fetch_shared_playlist(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXSharedPlaylistFetcher(token)
        playlist_id = '4nUZM-TY2aVxZ2xaA-'
        playlist = fetcher.fetch_shared_playlist(playlist_id)
        self._validate_playlist(playlist)
        next_page_data = fetcher.fetch_next_page(playlist['tracks'])
        self._validate_track_paging(next_page_data)
    
    def test_fetch_tracks_of_shared_playlist(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXSharedPlaylistFetcher(token)
        playlist_id = '4nUZM-TY2aVxZ2xaA-'
        tracks = fetcher.fetch_tracks_of_shared_playlists(playlist_id)
        self._validate_track_paging(tracks)
        next_page_data = fetcher.fetch_next_page(tracks)
        self._validate_track_paging(next_page_data)       

    def test_search(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXSearchFetcher(token)
        results = fetcher.search('love',
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
        if results['tracks']['paging']['next'] != None:            
            next_url = results['tracks']['paging']['next']
            next_result = fetcher.fetch_data(next_url)
            assert(next_result != None)

    def test_fetch_charts(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXChartFetcher(token)
        charts = fetcher.fetch_charts()
        self._validate_playlist_paging(charts)
        next_page_data = fetcher.fetch_next_page(charts)
        self._validate_playlist_paging(next_page_data)

    def test_fetch_charts_playlist(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXChartFetcher(token)
        playlist_id = '0kTVCy_kzou3AdOsAc'
        playlist = fetcher.fetch_charts_playlist(playlist_id)
        self._validate_playlist(playlist)
        next_page_data = fetcher.fetch_next_page(playlist['tracks'])
        self._validate_track_paging(next_page_data)

    def test_fetch_charts_playlist_tracks(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXChartFetcher(token)
        playlist_id = '0kTVCy_kzou3AdOsAc'
        playlist = fetcher.fetch_charts_playlist_tracks(playlist_id)
        self._validate_track_paging(playlist)
        next_page_data = fetcher.fetch_next_page(playlist)
        self._validate_track_paging(next_page_data)

    def test_fetch_all_new_release_categories(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXNewReleaseCategoryFetcher(token)
        categories = fetcher.fetch_all_new_release_categories()
        self._validate_category_paging(categories)
        next_page_data = fetcher.fetch_next_page(categories)
        self._validate_category_paging(next_page_data)

    def test_fetch_new_release_category(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXNewReleaseCategoryFetcher(token)
        category_id = '1ZQwmFTaLE4p7BG-Ua'
        category = fetcher.fetch_new_release_category(category_id)
        self._validate_category(category)
        next_page_data = fetcher.fetch_next_page(category['albums'])
        self._validate_album_paging(next_page_data)

    def test_fetch_albums_of_new_release_category(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXNewReleaseCategoryFetcher(token)
        category_id = '1ZQwmFTaLE4p7BG-Ua'
        albums = fetcher.fetch_albums_of_new_release_category(category_id)
        self._validate_album_paging(albums)
        next_page_data = fetcher.fetch_next_page(albums)
        self._validate_album_paging(next_page_data)

    def test_fetch_all_genre_stations(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXGenreStationFetcher(token)
        genre_stations = fetcher.fetch_all_genre_stations()
        self._validate_genre_station_paging(genre_stations)
        next_page_data = fetcher.fetch_next_page(genre_stations)
        self._validate_genre_station_paging(next_page_data)

    def test_fetch_genre_station(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXGenreStationFetcher(token)
        station_id = 'TYq3EHFTl-1EOvJM5Y'
        station = fetcher.fetch_genre_station(station_id)
        keys = ('category', 'tracks', 'id', 'name')
        for key in keys:
            assert key in station
        tracks = station['tracks']['data']
        for track in tracks:
            self._validate_track(track)

    def test_fetch_all_mood_stations(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXMoodStationFetcher(token)
        mood_stations = fetcher.fetch_all_mood_stations()
        self._validate_mood_station_paging(mood_stations)
        next_page_data = fetcher.fetch_next_page(mood_stations)
        self._validate_mood_station_paging(next_page_data)

    def test_fetch_mood_station(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXMoodStationFetcher(token)
        station_id = 'StGZp2ToWq92diPHS7'
        station = fetcher.fetch_mood_station(station_id)
        keys = ('tracks', 'id', 'name')
        for key in keys:
            assert key in station
        for track in station['tracks']['data']:
            self._validate_track(track)

    def test_fetch_all_feature_playlists(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXFeaturePlaylistFetcher(token)
        feature_playlists = fetcher.fetch_all_feature_playlists()
        self._validate_playlist_paging(feature_playlists)
        next_page_data = fetcher.fetch_next_page(feature_playlists)
        self._validate_playlist_paging(next_page_data)

    def test_fetch_feature_playlist(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXFeaturePlaylistFetcher(token)
        playlist_id = 'Wt95My35CqR9hB_FW1'
        feature_playlist = fetcher.fetch_feature_playlist(playlist_id)
        self._validate_playlist(feature_playlist)
        next_page_data = fetcher.fetch_next_page(feature_playlist['tracks'])
        self._validate_track_paging(next_page_data)

    def test_fetch_feature_playlist_tracks(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXFeaturePlaylistFetcher(token)
        playlist_id = 'Wt95My35CqR9hB_FW1'
        feature_playlist = fetcher.fetch_feature_playlist_tracks(playlist_id)
        self._validate_track_paging(feature_playlist)
        next_page_data = fetcher.fetch_next_page(feature_playlist)
        self._validate_track_paging(next_page_data)

    def test_fetch_categories_of_feature_playlist(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXFeaturePlaylistCategoryFetcher(token)
        categories = fetcher.fetch_categories_of_feature_playlist()
        self._validate_category_paging(categories)
        next_page_data = fetcher.fetch_next_page(categories)
        self._validate_category_paging(next_page_data)

    def test_fetch_feature_playlist_by_category(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXFeaturePlaylistCategoryFetcher(token)
        category_id = '9XQKD8BJx595ESs_rb'
        category = fetcher.fetch_feature_playlist_by_category(category_id)
        keys = ('id', 'title', 'images', 'playlists')
        for key in keys:
            assert key in category, 'missing key ' + key
        for image in category['images']:
            self._validate_image(image)
        for playlist in category['playlists']['data']:
            self._validate_playlist(playlist)

    def test_fetch_playlists_of_feature_playlist_category(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXFeaturePlaylistCategoryFetcher(token)
        category_id = '9XQKD8BJx595ESs_rb'
        category = fetcher.fetch_playlists_of_feature_playlist_category(category_id)
        self._validate_playlist_paging(category)
        next_page_data = fetcher.fetch_next_page(category)
        self._validate_playlist_paging(next_page_data)

    def test_fetch_all_new_hits_playlists(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXNewHitsPlaylistFetcher(token)
        new_hits = fetcher.fetch_all_new_hits_playlists()
        self._validate_playlist_paging(new_hits)
        next_page_data = fetcher.fetch_next_page(new_hits)
        self._validate_playlist_paging(next_page_data)

    def test_fetch_new_hits_playlist(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXNewHitsPlaylistFetcher(token)
        playlist_id = 'DZrC8m29ciOFY2JAm3'
        new_hits = fetcher.fetch_new_hits_playlist(playlist_id)
        self._validate_playlist(new_hits)
        next_page_data = fetcher.fetch_next_page(new_hits['tracks'])
        self._validate_track_paging(next_page_data)

    def test_fetch_new_hits_playlist_track(self):
        auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
        token = auth.fetch_access_token_by_client_credentials()
        fetcher = KKBOXNewHitsPlaylistFetcher(token)
        playlist_id = 'DZrC8m29ciOFY2JAm3'
        new_hits = fetcher.fetch_new_hits_playlist_tracks(playlist_id)
        self._validate_track_paging(new_hits)
        next_page_data = fetcher.fetch_next_page(new_hits)
        self._validate_track_paging(next_page_data)




if __name__ == '__main__':
    unittest.main()