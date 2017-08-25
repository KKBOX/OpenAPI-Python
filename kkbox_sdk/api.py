#!/usr/bin/env python
# encoding: utf-8

from auth_flow import *
from device_flow import *
from track_fetcher import *
from artist_fetcher import *
from album_fetcher import *
from shared_playlist_fetcher import *
from search_fetcher import *
from chart_fetcher import *
from new_release_category_fetcher import *
from genre_station_fetcher import *
from mood_station_fetcher import *
from feature_playlist_fetcher import *
from feature_playlist_category_fetcher import *
from new_hits_playlist_fetcher import *


class KKBOXAPI:
    '''
    Create fetchers.
    '''
    def __init__(self, access_token):

        self.http = KKBOXHTTP(access_token)

        self.search_fetcher = KKBOXSearchFetcher(access_token)

        self.track_fetcher = KKBOXTrackFetcher(access_token)

        self.artist_fetcher = KKBOXArtistFetcher(access_token)

        self.album_fetcher = KKBOXAlbumFetcher(access_token)

        self.shared_playlist_fetcher = KKBOXSharedPlaylistFetcher(access_token)

        self.chart_fetcher = KKBOXChartFetcher(access_token)

        self.new_release_category_fetcher = KKBOXNewReleaseCategoryFetcher(access_token)

        self.genre_station_fetcher = KKBOXGenreStationFetcher(access_token)

        self.mood_station_fetcher = KKBOXMoodStationFetcher(access_token)

        self.feature_playlist_fetcher = KKBOXFeaturePlaylistFetcher(access_token)

        self.feature_playlist_category_fetcher = KKBOXFeaturePlaylistCategoryFetcher(access_token)

        self.new_hits_playlist_fetcher = KKBOXNewHitsPlaylistFetcher(access_token)




