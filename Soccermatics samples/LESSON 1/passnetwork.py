# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 15:48:00 2022

@author: dev
"""

import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Pitch, Sbopen
import pandas as pd
import json

match_id = 69301
with open('E:/SoccermaticsForPython-master/statsbomb/data/events/'+str(match_id)+'.json') as d1:
    data = json.load(d1)
    
from pandas import json_normalize
df = json_normalize(data, sep = "_").assign(match_id = str(match_id)+'.json'[:-5])

#Passes = df.loc[df['type_name'] != 'Starting XI'].set_index('id')
#df1= df.drop(df[(df.type_name == 'Starting XI') & (df.type_name =='Half Start')].index)
#df = df.drop([df.index[0],df.index[1],df.index[2],df.index[3]])
Passes = df.loc[df['type_name'] == 'Pass'].set_index('id')

#index of first substitution
sub = df.loc[df["type_name"] == "Substitution"].loc[df["team_name"] == "England Women's"].iloc[0]["index"]
#making true and false values
mask_england = (df.type_name == 'Pass') & (df.team_name == "England Women's") & (df.index < sub)

#ValueError: Unable to parse string "an" at position 0
df['location'] = df['location'].fillna(0)
df['pass_end_location'] = df['pass_end_location'].fillna(0)

df["startX"] = df["location"].apply(str).str.split(", ", expand=True)[0].str[1:].apply(pd.to_numeric)
df["startY"] = df["location"].apply(str).str.split(", ", expand=True)[1].str[:-1].apply(pd.to_numeric)
df["endX"] = df["pass_end_location"].apply(str).str.split(", ", expand=True)[0].str[1:].apply(pd.to_numeric)
df["endY"] = df["pass_end_location"].apply(str).str.split(", ", expand=True)[1].str[:-1].apply(pd.to_numeric)


df_pass = df.loc[mask_england, ['startX', 'startY', 'endX', 'endY', "player_name", "pass_recipient_name"]]
df_pass["player_name"] = df_pass["player_name"].apply(lambda x: str(x).split()[-1])
df_pass["pass_recipient_name"] = df_pass["pass_recipient_name"].apply(lambda x: str(x).split()[-1])

scatter_df = pd.DataFrame()
for i, name in enumerate(df_pass["player_name"].unique()):
    passx = df_pass.loc[df_pass["player_name"] == name]["startX"].to_numpy()
    recx = df_pass.loc[df_pass["pass_recipient_name"] == name]["endX"].to_numpy()
    passy = df_pass.loc[df_pass["player_name"] == name]["startY"].to_numpy()
    recy = df_pass.loc[df_pass["pass_recipient_name"] == name]["endY"].to_numpy()
    scatter_df.at[i, "player_name"] = name
    #make sure that x and y location for each circle representing the player is the average of passes and receptions
    scatter_df.at[i, "x"] = np.mean(np.concatenate([passx, recx]))
    scatter_df.at[i, "y"] = np.mean(np.concatenate([passy, recy]))
    #calculate number of passes
    scatter_df.at[i, "no"] = df_pass.loc[df_pass["player_name"] == name].count().iloc[0]

scatter_df['marker_size'] = (scatter_df['no'] / scatter_df['no'].max() * 1500)

#counting passes between players
df_pass["pair_key"] = df_pass.apply(lambda startX: "_".join(sorted([startX["player_name"], startX["pass_recipient_name"]])), axis=1)
lines_df = df_pass.groupby(["pair_key"]).startX.count().reset_index()
lines_df.rename({'startX':'pass_count'}, axis='columns', inplace=True)
#setting a treshold. You can try to investigate how it changes when you change it.
lines_df = lines_df[lines_df['pass_count']>2]


#Drawing pitch

from mplsoccer.pitch import Pitch
import matplotlib.pyplot as plt

pitch = Pitch(line_color='grey')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)

#Scatter the location on the pitch
pitch.scatter(scatter_df.x, scatter_df.y, s=scatter_df.marker_size, color='red', edgecolors='grey', linewidth=1, alpha=1, ax=ax["pitch"], zorder = 3)

#annotating player name
for i, row in scatter_df.iterrows():
    pitch.annotate(row.player_name, xy=(row.x, row.y), c='black', va='center', ha='center', weight = "bold", size=16, ax=ax["pitch"], zorder = 4)

for i, row in lines_df.iterrows():
        player1 = row["pair_key"].split("_")[0]
        player2 = row['pair_key'].split("_")[1]
        #skippin the nan
        if (player2 == 'nan'):
            pass
        else:
        #take the average location of players to plot a line between them
            player1_x = scatter_df.loc[scatter_df["player_name"] == player1]['x'].iloc[0]
            player1_y = scatter_df.loc[scatter_df["player_name"] == player1]['y'].iloc[0]
            player2_x = scatter_df.loc[scatter_df["player_name"] == player2]['x'].iloc[0]
            player2_y = scatter_df.loc[scatter_df["player_name"] == player2]['y'].iloc[0]
            num_passes = row["pass_count"]
            #adjust the line width so that the more passes, the wider the line
            line_width = (num_passes / lines_df['pass_count'].max() * 10)
            #plot lines on the pitch
            pitch.lines(player1_x, player1_y, player2_x, player2_y,alpha=1, lw=line_width, zorder=2, color="grey", ax = ax["pitch"])

fig.suptitle("Pass network of England against Sweden", fontsize = 30)
plt.show()

##  CENTRALIZATION INDEX ##

#calculate number of successful passes by player
no_passes = df_pass.groupby(['player_name']).startX.count().reset_index()
no_passes.rename({'startX':'pass_count'}, axis='columns', inplace=True)
#find one who made most passes
max_no = no_passes["pass_count"].max()
#calculate the denominator - 10*the total sum of passes
denominator = 10*no_passes["pass_count"].sum()
#calculate the nominator
nominator = (max_no - no_passes["pass_count"]).sum()
#calculate the centralisation index
centralisation_index = nominator/denominator
print("Centralisation index is ", centralisation_index)