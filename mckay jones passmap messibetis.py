# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 18:06:21 2021

@author: dev
"""
#mckay jones into spyder

import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch

df = pd.read_csv('C:/Users/dev/Desktop/messibetis.csv')
df['x'] = df['x']*1.2
df['y'] = df['y']*0.8
df['endX'] = df['endX']*1.2
df['endY'] = df['endY']*0.8

pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc',figsize=(16, 11), constrained_layout=True, tight_layout=False)
pitch.draw()

for x in range(len(df['x'])):
    if df['outcome'][x] == 'Successful':
        plt.plot((df['x'][x],df['endX'][x]),(df['y'][x],df['endY'][x]),color='green')
        plt.scatter(df['x'][x],df['y'][x],color='Black')
        
plt.title('messi passes vs betis',color='Black',fontsize=25)