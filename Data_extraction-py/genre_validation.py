#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 15:52:45 2024

@author: kennedy
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import os.path
from ratelimit import limits, sleep_and_retry

# 180 calls per minute
CALLS = 180
RATE_LIMIT = 60

filename = 'genres/genres.txt'
genres = []
with open(filename, 'r') as file:
    for line in file.readlines():
        line = line.strip().replace(" ", "%")

        genres.append(line.strip())



cid = cid
secret = secret

client_credentials_manager = SpotifyClientCredentials(client_id=cid, 
                                                      client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager,
                     requests_timeout = None, retries = 0)



@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def check_limit():
    return



def validate_genres(genre_list, max_check = False):
    """
    Confirms which genres within the genre list have output in Spotify API, and
    returns a modified genre list for further data retrieval. Designed to work
    around API call limits by running based off previous progress.

    Parameters
    ----------
    genre_list : list
        A list of strings, genres to search with Spotify's API

    Returns
    -------
    None, writes file of valid genres into directory

    """
    check_limit()

    index = -1
    query_limit = 1
    query_offset = 0
    if os.path.isfile("validating_genres.txt"): 
        
        file_check = open("validating_genres.txt", "r")
        if file_check.readline() != "":
            for line in file_check:
                pass
            last_genre_checked = line
    
        file_check.close()
    # If true, checks for which genres reach max search values rather than whether
    # Spotify returns results. Used for later validation of genres that could
    # have more samples added.
    if max_check == True:
        query_limit = 50
        query_offset = 950
    file = open("validating_genres.txt", "a")
    
    if 'last_genre_checked' in locals(): 
        index = genre_list.index(last_genre_checked)
    print(index)
    for genre in genre_list[index + 1:]:
        print(genre)
        track_results = sp.search(q=f"genre:{genre}", type='track', 
                                  offset = query_offset,limit = query_limit)

        if track_results['tracks']['items'] != []:
            file.write(f"\n{genre}")
        else:
            with open("not_maxed_genres.txt", 'a') as file:
                file.write(f"\n{genre}")
        

def main():
    start = time.time()
    validate_genres(genres, max_check = True)


    print(time.time() - start)

    
main()