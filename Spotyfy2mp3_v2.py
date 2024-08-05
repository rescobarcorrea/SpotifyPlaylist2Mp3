# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 11:08:28 2024

@author: r_esc
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This script downloads a Spotify playlist to mp3 version 2

It first reads the Spotify list of songs from the playlist,
then searches it on YouTube,
then downloads it,
and finally sets the tags for Windows.

Tags fixed
rescobarcorrea@gmail.com
"""
# 0. Import libraries

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
import os
from os.path import exists
import pytube as pt
import mutagen
from mutagen.easyid3 import EasyID3

# 1. First step, reads songs from Spotify playlist

# Authentication, Create a Spotify developer profile and authenticate from there
cid='c5f72cc588ff445fbeXXXXXXXXXXXXXXXXXXXXXX'
secret='003d15369a3f44aXXXXXXXXXXXXXXXXXXXXXX'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Select your own playlist link here
playlist_link = "https://open.spotify.com/playlist/1So0sYHXBrByMvokIl5RxR?si=a2ae3c8de2604f87"

playlist_URI = playlist_link.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

destination_folder = r"C:\Users\r_esc\Music\downloads"
results = sp.playlist_items(playlist_URI)

track_list = results["items"]
while results['next']:
    results = sp.next(results)
    track_list.extend(results['items'])

for track in track_list:
    # Track name
    track_name = track["track"]["name"]
    
    # Artist name
    artist_name = track["track"]["artists"][0]["name"]

    print(track_name + ' - 'artist_name)
    # Album name
    album = track["track"]["album"]["name"]
    release_date = track["track"]["album"]['release_date']
    
    # Popularity of the track
    track_pop = track["track"]["popularity"]
    
    # Search URL
    videosSearch = VideosSearch(track_name + ' - ' + artist_name, limit=1)
    searched_result_url = videosSearch.result()["result"][0]["link"]
    
    # Download URL
    yt = pt.YouTube(searched_result_url)
    video = yt.streams.filter(only_audio=True).first()
    
    # Check if file doesn't exist
    potential_download_name = os.path.join(destination_folder, video.default_filename)
    base_p, ext_p = os.path.splitext(potential_download_name)
    new_file_p = base_p + '.mp3'
    
    if os.path.exists(new_file_p):
        print('-already downloaded')
    else:
        # Fixes extension
        out_file = video.download(output_path=destination_folder)
    
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        try:
            os.rename(out_file, new_file)
        except FileExistsError:
            continue
        print(yt.title + " has been successfully downloaded.")
        
        # Set tags using mutagen
        audio = EasyID3(new_file)
        audio['title'] = track_name
        audio['artist'] = artist_name
        audio['album'] = album
        audio['date'] = release_date
        audio.save()

print("All tracks have been downloaded and tagged.")