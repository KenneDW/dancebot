#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 10:26:26 2024

@author: kennedy
"""

import json



titles = []
with open("work", "r") as file:
    
    for line in file:
        
        info = json.loads(line)

        titles.append(info["title"])


with open("song_titles.txt", 'w') as supra_file:
    
    for title in titles:
        supra_file.write(f"{title}\n")
        