#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 13:45:37 2024

@author: kennedy
"""
import numpy.dtypes
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly

# Have code that has unique RGB values for each genre. These should be decided 
# based on the (x,y,z) values that each genre is plotted on.

# We want a function that creates a 3-dimensional, interactable (can be moved
# on the axis, zoomed in and out, etc.) graph that shows all genres on spotify
# mapped based on Spotify's attributes.

# We want to include a section that describes how many genres have the max
# sample size (n = 1000), the ratio of that to the total number of genres, and
# how many genres have less than that sample size. Print the genre with the 
# lowest sample size and have a message explaining that it is because Spotify
# does not have enough songs for every listed genre.

# Hypothetically, what would it be like to run KNN on song data? If we take half
# of the songs as training data, could we use certain attributes to establish
# some sort of correlation in correctly grouping them?

# Add option to randomly sample within each genre, as a way of ensuring an identical sample size
# for each genre

# Design these functions to be malleable, so we can import them into different python projects
# that target different approaches to the data.

def data_initiation(file):
    df = pd.read_csv(file)

    return df

def genre_sample_detection(df):
    # This function will determine the number of songs sampled from each genre
    counts = df['Genre'].value_counts()

    return counts

def genre_aggregation(df, rounds=3):
    # This function should take each song entry under a Genre, and aggregate them under
    # said genre to produce a sample of that genre's metrics.
    genres = df['Genre'].unique()
    # Drop columns that cannot be aggregated
    for key, value in df.dtypes.items():
        if not isinstance(value, (numpy.dtypes.Float64DType, numpy.dtypes.Int64DType)) and key != 'Genre':
            df = df.drop(key, axis=1)

    avg_df = pd.DataFrame()
    for genre in genres:
        genre_df = df.loc[df['Genre'] == genre]
        genre_df.set_index('Genre', inplace=True)
        # Get average metrics and return as a DataFrame of that genre
        genre_df = genre_df.mean().round(rounds).to_frame().T
        genre_df.rename(index={0:genre}, inplace=True)
        avg_df = pd.concat([avg_df, genre_df])

    return avg_df

def add_counts(counts, df):
    # Adds the sample size of each genre to each averaged genre row
    df.insert(0, 'Sample Size', counts.values)
    return df

def save_to_csv(df, filename = 'spotify_genre_averages.csv'):
    # Used to export dataframe data to CSV
    df.to_csv(filename)

def main():
    df_data = data_initiation('spotify_song_data_9_19.csv')
    # For the final exported csv, we should include the sample size used for each genre for the averages
    counts = genre_sample_detection(df_data)
    genre_avgdata = genre_aggregation(df_data)
    final_data = add_counts(counts, genre_avgdata)
    save_to_csv(final_data)

if __name__ == '__main__':
    main()