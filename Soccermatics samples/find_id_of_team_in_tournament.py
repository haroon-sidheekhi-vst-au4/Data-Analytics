# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 19:42:29 2022

@author: dev
"""


import matplotlib.pyplot as plt
from mplsoccer import Pitch, Sbopen
import pandas as pd
parser = Sbopen()

import json
from pandas import json_normalize

with open('E:\SoccermaticsForPython-master\statsbomb01\data\competitions.json') as d1:
    competitions = json.load(d1)
    
competition_id=55
season_id=43
with open('E:/SoccermaticsForPython-master/statsbomb01/data/matches/'+str(competition_id)+'/'+str(season_id)+'.json',encoding="utf8") as d2:
    matches = json.load(d2)    
df_match = json_normalize(matches, sep = "_")

team = "Italy"
match_ids = df_match.loc[(df_match["home_team_home_team_name"] == team) | (df_match["away_team_away_team_name"] == team)]["match_id"].tolist()
no_games = len(match_ids)
