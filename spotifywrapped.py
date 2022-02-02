#!/usr/bin/env python
# coding: utf-8

import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time
import datetime
import gspread

SPOTIPY_CLIENT_ID='removed'
SPOTIPY_CLIENT_SECRET='removed'
SPOTIPY_REDIRECT_URI='removed '
SCOPE = "user-top-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI,scope=SCOPE))

#gets list of the ids from top songs/artists from a given time frame
def get_track_ids(time_frame):
    track_ids = []
    for song in time_frame['items']:
        track_ids.append(song['id'])
    return track_ids

def get_artist_ids(time_frame):
    artist_ids = []
    for artist in time_frame['items']:
        artist_ids.append(artist['id'])
    return artist_ids

#gets needed track/artist data from given id
def get_track_features(id):
    meta = sp.track(id)
    # meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    spotify_url = meta['external_urls']['spotify']
    album_cover = meta['album']['images'][0]['url']
    track_info = [name,album,artist, spotify_url, album_cover]
    return track_info

def get_artist_features(id):
    meta = sp.artist(id)
    # meta
    name = meta['name']
    spotify_url = meta['external_urls']['spotify']
    artist_image = meta['images'][0]['url']
    artist_info = [name,spotify_url, artist_image]
    return artist_info


# test run: loop over track ids
tracks = []
for i in range(len(track_ids)):
        time.sleep(.5)
        track = get_track_features(track_ids[i])
        tracks.append(track)                              


#insert tracks/artists to gooogle sheets
def insert_to_gsheet(track_ids):
 # loop over track ids 
 tracks = []
 for i in range(len(track_ids)):
     time.sleep(.5)
     track = get_track_features(track_ids[i])
     tracks.append(track)
 # create dataset
 df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'spotify_url', 'album_cover'])
 # insert into google sheet
 gc = gspread.service_account(filename='removed')
 sh = gc.open('My Spotify Wrapped')
 worksheet = sh.worksheet(f'{time_period}')
 worksheet.update([df.columns.values.tolist()] + df.values.tolist())

def insert_to_gsheet(artist_ids):
     artists = []
     for i in range(len(artist_ids)):
         time.sleep(.5)
         artist = get_artist_features(artist_ids[i])
         artists.append(artist)
     artists_df = pd.DataFrame(artists, columns = ['name','spotify_url', 'aartist_image'])
     gc = gspread.service_account(filename='removed')
     sh = gc.open('My Spotify Wrapped')
     worksheet = sh.worksheet('artists_' + f'{time_period}')
     worksheet.update([artists_df.columns.values.tolist()] + artists_df.values.tolist())

time_ranges = ['short_term', 'medium_term', 'long_term']

#run following in jupyter notebook to update data in gsheet
for time_period in time_ranges:
     top_tracks = sp.current_user_top_tracks(limit=20, offset=0, time_range=time_period)
     track_ids = get_track_ids(top_tracks)
     insert_to_gsheet(track_ids)

for time_period in time_ranges:
     top_artists = sp.current_user_top_artists(limit=20, offset=0, time_range=time_period)
     artist_ids = get_artist_ids(top_artists)
     insert_to_gsheet(artist_ids)




