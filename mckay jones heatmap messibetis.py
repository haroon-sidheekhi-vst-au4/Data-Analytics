# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 01:40:24 2021

@author: dev
"""

#mckay jones into spyder

import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
import seaborn as sns

df = pd.read_csv('C:/Users/dev/Desktop/messibetis.csv')
df['x'] = df['x']*1.2
df['y'] = df['y']*0.8
df['endX'] = df['endX']*1.2
df['endY'] = df['endY']*0.8
fig,ax= plt.subplots(figsize=(13,8.5))
fig.set_facecolor('#22312b')
ax.patch.set_facecolor('#22312b')

pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc',figsize=(16, 11), constrained_layout=True, tight_layout=False)
pitch.draw(ax=ax)
plt.gca().invert_yaxis()
kde = sns.kdeplot(
    df['x'],
    df['y'],
    shade=True,
    shade_lowest=False,
    alpha=0.5,
    n_levels=11,
    cmap = 'magma'
    )
for x in range(len(df['x'])):
    if df['outcome'][x] == 'Successful':
        plt.plot((df['x'][x],df['endX'][x]),(df['y'][x],df['endY'][x]),color='green')
        plt.scatter(df['x'][x],df['y'][x],color='Black')
plt.xlim(0,120)
plt.ylim(0,80)        
plt.title('Messi heatmap vs betis',color='White',size=25)