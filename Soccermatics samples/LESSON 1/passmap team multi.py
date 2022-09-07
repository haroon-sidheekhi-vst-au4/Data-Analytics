# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 23:05:05 2022

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

Passes["startX"] = Passes["location"].apply(str).str.split(", ", expand=True)[0].str[1:].apply(pd.to_numeric)
Passes["startY"] = Passes["location"].apply(str).str.split(", ", expand=True)[1].str[:-1].apply(pd.to_numeric)
Passes["endX"] = Passes["pass_end_location"].apply(str).str.split(", ", expand=True)[0].str[1:].apply(pd.to_numeric)
Passes["endY"] = Passes["pass_end_location"].apply(str).str.split(", ", expand=True)[1].str[:-1].apply(pd.to_numeric)

#prepare the dataframe of passes by England that were no-throw ins
mask_england = (Passes.type_name == 'Pass') & (Passes.team_name == "England Women's")
Passes_passes = Passes.loc[mask_england, ['startX', 'startY', 'endX', 'endY', 'player_name']]
#get the list of all players who made a pass
names = Passes_passes['player_name'].unique()

#draw 4x4 pitches
from mplsoccer.pitch import Pitch
import matplotlib.pyplot as plt
pitch = Pitch(line_color='black', pad_top=20)
fig, axs = pitch.grid(ncols = 4, nrows = 4, grid_height=0.85, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0.04, endnote_space=0.01)

#for each player
for name, ax in zip(names, axs['pitch'].flat[:len(names)]):
    #put player name over the plot
    ax.text(60, -10, name,
            ha='center', va='center', fontsize=14)
    #take only passes by this player
    player_df = Passes_passes.loc[Passes_passes["player_name"] == name]
    #scatter
    pitch.scatter(player_df.startX, player_df.startY, alpha = 0.2, s = 50, color = "blue", ax=ax)
    #plot arrow
    pitch.arrows(player_df.startX, player_df.startY,
            player_df.endX, player_df.endY, color = "blue", ax=ax, width=1)

#We have more than enough pitches - remove them
for ax in axs['pitch'][-1, 16 - len(names):]:
    ax.remove()

#Another way to set title using mplsoccer
axs['title'].text(0.5, 0.5, 'England passes against Sweden', ha='center', va='center', fontsize=30)
plt.show()