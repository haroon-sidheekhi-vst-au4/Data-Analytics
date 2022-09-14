# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 23:32:41 2022

@author: dev
"""

import matplotlib.pyplot as plt
from mplsoccer import Pitch
import pandas as pd

import json
from pandas import json_normalize

with open('E:\SoccermaticsForPython-master\statsbomb\data\competitions.json') as d1:
    competitions = json.load(d1)
    
competition_id=72
season_id=30
with open('E:/SoccermaticsForPython-master/statsbomb/data/matches/'+str(competition_id)+'/'+str(season_id)+'.json') as d2:
    matches = json.load(d2)    
df_match = json_normalize(matches, sep = "_")

#list of match id's
team = "England Women's"
match_ids = df_match.loc[(df_match["home_team_home_team_name"] == team) | (df_match["away_team_away_team_name"] == team)]["match_id"].tolist()
no_games = len(match_ids)
