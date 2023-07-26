# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 19:51:33 2023

@author: hp
"""

import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch
import mplsoccer

MATCH_ID = 3788741

#Turkey     3788741
#Switzerland 3788754		
#Austria	 3794685		
#Belgium		3795107	

#match_events_df = sb.events(match_id = MATCH_ID)
file_name=str(MATCH_ID)+'.json'


#event data

import json
with open('E:/Docs/Data/Github/open-data/data/events/'+str(MATCH_ID)+'.json') as f:
    data = json.load(f)
from pandas.io.json import json_normalize
from pandas.io import json
match_events_df = json_normalize(data, sep = "_").assign(match_id = file_name[:-5])


#360 data

match_360_df = pd.read_json(f'E:/Docs/Data/Github/open-data/data/three-sixty/{MATCH_ID}.json')

#data integration into one central location

df = pd.merge(left=match_events_df, right=match_360_df, left_on='id', right_on='event_uuid', how='left')

#Displaying passes made by Locatelli


player1_df = df[(df['pass_recipient_name'] == 'Leonardo Spinazzola') & (df['type_name'] == 'Pass')].reset_index(drop=True)

player1_df[['x_start','y_start']] = pd.DataFrame(player1_df.location.tolist(), index=player1_df.index)
player1_df[['x_end','y_end']] = pd.DataFrame(player1_df.pass_end_location.tolist(), index=player1_df.index)


pitch = mplsoccer.VerticalPitch(pitch_type= 'statsbomb',pitch_color='black',line_color='White')
fig,ax = pitch.draw(figsize=(13,8))

pitch.lines(player1_df['x_start'],player1_df['y_start'],
                 player1_df['x_end'],player1_df['y_end'],
                comet=True,transparent =True,alpha_start=0.1,alpha_end=0.4,
                 color='white',alpha=0.3,
                zorder = 2, ax=ax)
pitch.scatter(player1_df['x_end'],player1_df['y_end'],
             color='blue',edgecolor='black',ax=ax,
             s=100,lw=2,zorder = 3)

fig.suptitle('Pass receiving area of Leonardo Spinazzola\n Italy vs Turkey EURO 2020 | 12-06-2021 ')