#!/usr/bin/env python
# encoding: utf-8

from .auth_flow import *
from .track_fetcher import *
from .artist_fetcher import *
from .album_fetcher import *
from .shared_playlist_fetcher import *
from .search_fetcher import *
from .chart_fetcher import *
from .new_release_category_fetcher import *
from .genre_station_fetcher import *
from .mood_station_fetcher import *
from .feature_playlist_fetcher import *
from .feature_playlist_category_fetcher import *
from .new_hits_playlist_fetcher import *


class KKBOXAPI:
    '''
    Create fetchers.
    '''
    def __init__(self, access_token):
        #: The search related API fetcher
        self.search_fetcher = KKBOXSearchFetcher(access_token)
        #: The track related API fetcher
        self.track_fetcher = KKBOXTrackFetcher(access_token)
        #: The artist related API fetcher
        self.artist_fetcher = KKBOXArtistFetcher(access_token)
        #: The album related API fetcher
        self.album_fetcher = KKBOXAlbumFetcher(access_token)
        #: The shared playlist related API fetcher
        self.shared_playlist_fetcher = KKBOXSharedPlaylistFetcher(access_token)
        #: The chart related API fetcher
        self.chart_fetcher = KKBOXChartFetcher(access_token)
        #: The new release category related API fetcher
        self.new_release_category_fetcher = KKBOXNewReleaseCategoryFetcher(access_token)
        #: The genre station related API fetcher
        self.genre_station_fetcher = KKBOXGenreStationFetcher(access_token)
        #: The mood station related API fetcher
        self.mood_station_fetcher = KKBOXMoodStationFetcher(access_token)
        #: The feature playlist related API fetcher
        self.feature_playlist_fetcher = KKBOXFeaturePlaylistFetcher(access_token)
        #: The feature playlist category related API fetcher
        self.feature_playlist_category_fetcher = KKBOXFeaturePlaylistCategoryFetcher(access_token)
        #: The new hits playlist related API fetcher
        self.new_hits_playlist_fetcher = KKBOXNewHitsPlaylistFetcher(access_token)

