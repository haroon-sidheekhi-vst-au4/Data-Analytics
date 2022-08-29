# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 20:05:37 2022

@author: dev
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 01:24:28 2021

@author: dev
"""

import json
match_id = 7581
with open('E:/SoccermaticsForPython-master/statsbomb/data/events/'+str(match_id)+'.json',encoding="utf8") as f:
    data = json.load(f)
from pandas import json_normalize
df = json_normalize(data, sep = "_").assign(match_id = str(match_id)+'.json'[:-5])
df= df.loc[df['type_name'] == 'Shot'].set_index('id')

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

a_xg = [0]
h_xg = [0]
a_min = [0]
h_min = [0]

hteam = df['team_name'].iloc[0]
ateam = df['team_name'].iloc[1]

for x in range (len(df['shot_statsbomb_xg'])):
    if df['team_name'][x]==hteam:
            h_xg.append(df['shot_statsbomb_xg'][x])
            h_min.append(df['minute'][x])
    if df['team_name'][x]==ateam:
            a_xg.append(df['shot_statsbomb_xg'][x])
            a_min.append(df['minute'][x])            
            
def nums_cumulative_sum(nums_list):
    return [sum(nums_list[:i+1]) for i in range (len(nums_list))]

h_cumulative = nums_cumulative_sum(h_xg)
a_cumulative = nums_cumulative_sum(a_xg)

a_total = round(a_cumulative[-1],2)
h_total = round(h_cumulative[-1],2)

fig ,ax = plt.subplots(figsize=(10,6))
fig.set_facecolor('#22312b')
ax.patch.set_facecolor('#22312b')

plt.xticks([0,10,20,30,40,50,60,70,80,90,100,110,120])
plt.xlabel('Minute', color='white',fontsize='20')
plt.ylabel('xG', color='white',fontsize='20')
plt.title(hteam+' vs '+ateam+' xG')
ax.step(x=a_min,y=a_cumulative)
ax.step(x=h_min,y=h_cumulative)