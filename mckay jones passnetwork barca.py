# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 21:35:27 2021

@author: dev
"""

import pandas as pd
from mplsoccer.pitch import Pitch

df = pd.read_csv('E:\mckayjohnes\github\ValladolidA.csv')
df = df[df['teamId']=='Barcelona']

df['passer'] = df['playerId']
df['recepient'] = df['playerId'].shift(-1)

passes = df[df['type']=='Pass']
successful = passes[passes['outcome'] == 'Successful']

#finding the substite time and proceeding till that occures
subs = df[df['type'] == 'SubstitutionOff']
subs = subs['minute']
firstsub = subs.min()

successful = successful[successful['minute']<firstsub]

average_locations = successful.groupby('passer').agg({'x':['mean'],'y':['mean','count']})
average_locations.columns = ['x','y','count']
average_locations['passer'] = average_locations.index

# pasr = pd.to_numeric(average_locations['passer'],downcast='integer')
# average_locations['passer']= pasr

pass_between = successful.groupby(['passer','recepient']).id.count().reset_index()
pass_between.rename({'id':'pass_count'},axis = 'columns', inplace = True)

pass_between = pass_between.merge(average_locations, left_on= 'passer', right_index = True)
pass_between = pass_between.merge(average_locations, left_on= 'recepient', right_index = True,suffixes=['','_end'])

pass_between = pass_between[pass_between['pass_count']>3]

pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc',figsize=(16, 11), constrained_layout=True, tight_layout=False)
fig, ax = pitch.draw()
fig.set_facecolor("#22312b")

arrows = pitch.lines(1.2*pass_between.x,.8*pass_between.y,
                      1.2*pass_between.x_end,.8*pass_between.y_end,ax=ax,
                      lw = pass_between.pass_count*1, color = 'White',zorder =1, alpha= 0.5)
nodes = pitch.scatter(1.2*average_locations.x,.8*average_locations.y,s = 600,color = '#d3d3d3',
                      edgecolors= 'black',linewidth = 2.5, alpha = 1, ax=ax)
for index, row in average_locations.iterrows():
    pitch.annotate(int(row.passer), xy=(row.x*1.2, row.y*.8), c='Black', va='center',
                   ha='center', size=13, weight='bold', ax=ax)

ax.set_title('Barcelona vs Valladolida', color='#dee6ea',fontsize=30)
ax.set_xlabel('@ibramallu')
    
    
    