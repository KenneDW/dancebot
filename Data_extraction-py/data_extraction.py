#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 10:17:14 2024

@author: kennedy
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.client import SpotifyException
import time
from ratelimit import limits, sleep_and_retry
import csv
import os.path
import pandas as pd
from collections import Counter

cid = cid
secret = secret

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, 
                     requests_timeout = None, retries = 0)

CALLS = 180
RATE_LIMIT = 60

# Credit: https://stackoverflow.com/questions/40748687/python-api-rate-limiting-how-to-limit-api-calls-globally
@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def check_limit():
    return

def file_to_list(filename):
    """
    Takes valid genre list and returns genre as list

    Parameters
    ----------
    filename : file
        file of valid spotify API search genres

    Returns
    -------
    genres : list
        data from file as list

    """
    genres = []
    
    
    with open(filename, 'r') as file:
        for line in file.readlines():
            genres.append(line.strip())
    return genres

def index_check(file_name):
    """
    Checks and returns the last element written to a file

    Parameters
    ----------
    file_name : str
        a file

    Returns
    -------
    last_to_index : str
        the last element written to the file

    """
    
    if os.path.isfile(file_name): 
        # used for finding last genre checked for csv files in search
        if '.csv' in file_name:
            with open(file_name, 'r') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    pass
                if 'row' in locals():
                    if 'initial' in file_name:
                        last_to_index = row[0].replace(' ', '%')
                    else:
                        last_to_index = row[1]
                    return last_to_index
        # used for finding last index checked for additional data search
        if '.txt' in file_name:
            with open(file_name, 'r') as txt_file:
                lines = txt_file.readlines()
                if lines:
                    last_to_index = int(lines[-1])
                else: return
            return last_to_index
    
        else: 
            return
    else:
        file = open(file_name, 'w')
        file.close()
        index_check(file_name)

def initial_data(genre_list, sample_size = 1000, results_per_call = 50):
    """
    Function to sample songs from every available genre in Spotify's API and 
    save said data to a csv file.

    Parameters
    ----------
    genre_list : list
        list of genres assumed to be accessible within Spotify's API filter search.
    sample_size : int, optional
        the number of songs that will be sample from each genre. Minimum value
        of 1 and maximum value of 1,000.
    results_per_call : int, optional
        the number of results to be returned by the API query. Minimum value
        of 1 and maximum value of 50.
    Returns
    -------
    None, writes data to a file so it can be stored locally instead of on memory.

    """
    check_limit()

    
    genre_to_check = index_check("initiald_spotify_data.csv")
    
    if genre_to_check != None:
        print(genre_to_check)
        index = genre_list.index(genre_to_check)
    else:
        index = -1
    
    
    
    fields = ["Genre", "Track Name", "Track ID", "Artist", "Popularity"]
    
    with open("initiald_spotify_data.csv", "a", newline = '') as file:
        
        writer = csv.DictWriter(file, fieldnames=fields)
        
        if index == -1:
            writer.writeheader()
    
        for genre in genre_list[index + 1:]:
            for i in range(0, sample_size, 50):
                
                track_results = sp.search(q=f"genre:{genre}", type='track', 
                                          limit = results_per_call, offset = i)
                time.sleep(0.5)
                if track_results['tracks']['items'] != []:

                    for i, t in enumerate(track_results['tracks']['items']):
                        song = {}
                        
                        song["Genre"] = genre.replace("%", " ")
                        song['Track Name'] = t['name']
                        song['Track ID'] = t['id']
                        song['Artist'] = t['artists'][0]['name']
                        song['Popularity'] = t['popularity']
                        
                        writer.writerow(song)
                        
                        print(t['name'] + " Added")
                        
                else:   # If we've run through all the songs in the genre, stop sampling
                    break




def clean_initial_data(initial_file, new_file = 'full_initial_spotify_data.csv'):
    """
    Takes the genres that were skipped in the event of an error and 

    Parameters
    ----------
    initial_file : csv file string containing initial song information

    new_file: csv file string where we will write our final initial data


    Returns
    -------
    None, rewrites initial_file to include all song information
    
    """
    # Runs if there are missing genres to add

    # Read all of initial file 
    with open(initial_file, 'r') as file:
        reader = csv.reader(file)
        initial_lines = []
        for row in reader:
            initial_lines.append(row)

    # Read all of genres
    with open("valid_genres.txt", 'r') as file:
        old_genres = file.read().splitlines()
    
    # Count all occurences of genres throughout CSV
    genres_list = []
    for line in initial_lines:
        genres_list.append(line[0].replace(' ', '%'))
    counts = dict(Counter(genres_list))

    # Creates list of genres that need to be rewritten to the finished CSV
    genres_to_correct = []
    for genre in old_genres:
        # Check if a given genre needs to be added to the list
        if genre in counts:
            # Checks if given genre did not complete all samples before
            # error occurred.
            if counts[genre] != 1000:
                genres_to_correct.append(genre)
        else:
            genres_to_correct.append(genre)
    

    # Writes the final initial CSV
    with open(new_file, 'w') as file:
        writer = csv.writer(file)
        for line in initial_lines:
            # writes only complete genres
            if line[0].replace(' ', '%') not in genres_to_correct:
                writer.writerow(line)
                
        # prevent overusing memory
        del initial_lines
    
        fields = ["Genre", "Track Name", "Track ID", "Artist", "Popularity"]
        writer = csv.DictWriter(file, fieldnames = fields)
        
        for genre in genres_to_correct:
            for i in range(0, 1000, 50):
                track_results = sp.search(q=f"genre:{genre}", type='track', 
                                          limit = 50, offset = i)
                
                if track_results['tracks']['items'] != []:
                    for i, t in enumerate(track_results['tracks']['items']):
                        song = {}
                        
                        song["Genre"] = genre.replace("%", " ")
                        song['Track Name'] = t['name']
                        song['Track ID'] = t['id']
                        song['Artist'] = t['artists'][0]['name']
                        song['Popularity'] = t['popularity']
                        
                        writer.writerow(song)

def additional_song_data(genres_info_file, tracks_index = 100):
    """
    Takes the earlier Spotify API song data file as input, and finds Spotify's metrics
    for each song. Returns a new file containing additional data, namely the
    Spotify metrics for each song.

    Parameters
    ----------
    genres_info : csv file
        contains preliminary spotify data.
    tracks_index : int
        index for list slicing of track ids. Can be fed new indexing when function
        unexpectedly encounters an error. default is 100

    Returns
    -------
    New csv file containing all data/metrics needed from Spotify API

    """
    check_limit()

    # using pandas DataFrames to simplify process of file writing
    df = pd.read_csv(genres_info_file)
    
    track_ids = df['Track ID'].to_list()
    
    last_song = index_check('spotify_song_data.csv')
    
    file = open('spotify_song_data.csv', 'a')
    
    writer = csv.DictWriter(file, fieldnames=df.columns.to_list() + 
            ['Danceability', 'Energy', 'Speechiness', 'Acousticness', 
             'Instrumentalness', 'Liveness', 'Valence', 'Time Signature'])
    

    tracks_index = index_check('missing_song_indexes.txt')
    
    if tracks_index == None:
        tracks_index = 100
        
    if tracks_index == 100:
        writer.writeheader()
        index = 0
    else: index = int(tracks_index) - 100
    
    api_calls = 0
    
    for i in range(tracks_index, len(track_ids) + 100, 100):
        try:
            if i <= len(track_ids):

                # Use list slicing to minimize necessary API calls while maximizing
                # data retrieval
                total_features = []
                total_features.extend(sp.audio_features(tracks=track_ids[i - 100 : i]))
                time.sleep(0.5)
                api_calls += 1
                print(api_calls)
                
                for song in total_features:
                    df.loc[index, 'Danceability'] = song['danceability']
                    df.loc[index, 'Energy'] = song['loudness']
                    df.loc[index, 'Speechiness'] = song['speechiness']
                    df.loc[index, 'Acousticness'] = song['acousticness']
                    df.loc[index, 'Instrumentalness'] = song['instrumentalness']
                    df.loc[index, 'Liveness'] = song['liveness']
                    df.loc[index, 'Valence'] = song['valence']
                    df.loc[index, 'Time Signature'] = song['time_signature']

                    writer.writerow(df.iloc[index].to_dict())
                    
                    index += 1

                
            else: 
                i = len(track_ids)
                total_features.extend(sp.audio_features(tracks=track_ids[i - (i % 100) : i]))
                
                for song in total_features[i - (i % 100) : i]:
                    df.loc[index, 'Danceability'] = song['danceability']
                    df.loc[index, 'Energy'] = song['loudness']
                    df.loc[index, 'Speechiness'] = song['speechiness']
                    df.loc[index, 'Acousticness'] = song['acousticness']
                    df.loc[index, 'Instrumentalness'] = song['instrumentalness']
                    df.loc[index, 'Liveness'] = song['liveness']
                    df.loc[index, 'Valence'] = song['valence']
                    df.loc[index, 'Time Signature'] = song['time_signature']
                
                    writer.writerow(df.iloc[index].to_dict())
                
                    index += 1
        
        # Return last index so function can be re-run     
        except SpotifyException as err:
            print(vars(err))
            new_last_song = index_check('spotify_song_data.csv')
            if new_last_song != last_song:
                with open("missing_song_indexes.txt", 'a') as file:
                    file.write(str(i) + '\n')
            raise err




