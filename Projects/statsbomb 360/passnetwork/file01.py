# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 21:08:12 2023

@author: hp
"""

import pandas as pd
from mplsoccer.pitch import Pitch

MATCH_ID = 3788766				      #TUR
#match_events_df = sb.events(match_id = MATCH_ID)
file_name=str(MATCH_ID)+'.json'


import json
with open('E:/Docs/Data/Github/open-data/data/events/'+str(MATCH_ID)+'.json') as f:
    data = json.load(f)
from pandas.io.json import json_normalize
from pandas.io import json
match_events_df = json_normalize(data, sep = "_").assign(match_id = file_name[:-5])

match_360_df = pd.read_json(f'E:/Docs/Data/Github/open-data/data/three-sixty/{MATCH_ID}.json')

#data integration into one central location

df = pd.merge(left=match_events_df, right=match_360_df, left_on='id', right_on='event_uuid', how='left')

Italy_df = df[(df['possession_team_name'] == 'Italy') & (df['type_name'] == 'Pass')].reset_index(drop=True)

Italy_df['passer'] = Italy_df['player_id']
Italy_df['recipient'] = Italy_df ['player_id'].shift(-1)


subs = df[df['type_name']=='Substitution']
subs = subs['minute']
firstsub = subs.min()

Italy_df = Italy_df[Italy_df['minute']<firstsub]

Italy_df[['x','y']] = pd.DataFrame(Italy_df.location.tolist(), index=Italy_df.index)
Italy_df[['endX','endY']] = pd.DataFrame(Italy_df.pass_end_location.tolist(), index=Italy_df.index)

average_locations = Italy_df.groupby('passer').agg({'x':['mean'],'y':['mean','count']})
average_locations.columns = ['x','y','count']

pass_between = Italy_df.groupby(['passer','recipient']).id.count().reset_index()
pass_between.rename({'id':'pass_count'},axis='columns',inplace=True)
pass_between = pass_between.merge(average_locations, left_on = 'passer',right_index=True)
pass_between = pass_between.merge(average_locations, left_on = 'recipient',right_index=True,suffixes=['','_end'])
pass_between = pass_between[pass_between['pass_count']>1]
pass_between

pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
fig.set_facecolor("#22312b")

arrows = pitch.arrows(1.2*pass_between.x,0.8*pass_between.y,
                      1.2*pass_between.x_end,0.8*pass_between.y_end,ax=ax,
                     lw = pass_between.pass_count*1,headwidth = 3, color = 'w',zorder = 1, alpha=0.8)

nodes = pitch.scatter(1.2*pass_between.x,0.8*pass_between.y,
                     s=500, color = 'Black',edgecolors = 'gray', linewidth = 2.5, ax=ax)

ax.set_title('Italy vs Turkey', color='#dee6ea',fontsize=25)
