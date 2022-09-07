# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 17:54:33 2022

@author: dev
"""
import json
import pandas as pd 
match_id = 69301
with open('E:/SoccermaticsForPython-master/statsbomb/data/events/'+str(match_id)+'.json') as d1:
    data = json.load(d1)
from pandas import json_normalize
df = json_normalize(data, sep = "_").assign(match_id = str(match_id)+'.json'[:-5])
Passes = df.loc[df['type_name'] == 'Pass'].set_index('id')

team1, team2 = df.team_name.unique()

from mplsoccer.pitch import Pitch
import matplotlib.pyplot as plt
pitch = Pitch(line_color = "black")
fig, ax = pitch.draw(figsize=(10, 7))

Passes["startX"] = Passes["location"].apply(str).str.split(", ", expand=True)[0].str[1:].apply(pd.to_numeric)
Passes["startY"] = Passes["location"].apply(str).str.split(", ", expand=True)[1].str[:-1].apply(pd.to_numeric)
Passes["endX"] = Passes["pass_end_location"].apply(str).str.split(", ", expand=True)[0].str[1:].apply(pd.to_numeric)
Passes["endY"] = Passes["pass_end_location"].apply(str).str.split(", ", expand=True)[1].str[:-1].apply(pd.to_numeric)

mask_bronze = (Passes.type_name == 'Pass') & (Passes.player_name == "Lucy Bronze")
Passes_pass = Passes.loc[mask_bronze, ['startX', 'startY', 'endX', 'endY']]

pitch = Pitch(line_color='black')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
pitch.arrows(Passes_pass.startX, Passes_pass.startY,
            Passes_pass.endX, Passes_pass.endY, color = "blue", ax=ax['pitch'])
pitch.scatter(Passes_pass.startX, Passes_pass.startY, alpha = 0.2, s = 500, color = "blue", ax=ax['pitch'])
fig.suptitle("Lucy Bronze passes against Sweden", fontsize = 30)
plt.show()