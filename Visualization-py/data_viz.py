#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 13:45:37 2024

@author: kennedy
"""

import pandas as pd
import matplotlib.pyplot as plt

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