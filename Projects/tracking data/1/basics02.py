# -*- coding: utf-8 -*-
"""
Created on Tue May 23 00:39:45 2023

@author: hp
"""


import Metrica_IO as mio
import Metrica_Viz as mviz

DATADIR = 'E:/Docs/Data/metrica sports sample-data-master/data'
game_id = 2 # let's look at sample match 2

##event data loading
events = mio.read_event_data(DATADIR,game_id)
events = mio.to_metric_coordinates(events)

home_events = events[events['Team']=='Home']
away_events = events[events['Team']=='Away']

shots = events[events['Type']=='SHOT']
home_shots = home_events[home_events.Type=='SHOT']
away_shots = away_events[away_events.Type=='SHOT']

home_goals = home_shots[home_shots['Subtype'].str.contains('-GOAL')].copy()
away_goals = away_shots[away_shots['Subtype'].str.contains('-GOAL')].copy()


### 2nd home goal
fig,ax = mviz.plot_pitch()
ax.plot( events.loc[1118]['Start X'], events.loc[1118]['Start Y'], 'ro' )
ax.annotate("", xy=events.loc[1118][['End X','End Y']], xytext=events.loc[1118][['Start X','Start Y']], alpha=0.6, arrowprops=dict(arrowstyle="->",color='r'))
mviz.plot_events( events.loc[1115:1116], indicators = ['Marker','Arrow'], annotate=True,figax=(fig,ax) )


### 3rd home goal

fig,ax = mviz.plot_pitch()
ax.plot( events.loc[1723]['Start X'], events.loc[1723]['Start Y'], 'ro' )
ax.annotate("", xy=events.loc[1723][['End X','End Y']], xytext=events.loc[1723][['Start X','Start Y']], alpha=0.6, arrowprops=dict(arrowstyle="->",color='r'))
mviz.plot_events( events.loc[1719:1720], indicators = ['Marker','Arrow'], annotate=True,figax=(fig,ax) )
mviz.plot_events( events.loc[1722:1723], indicators = ['Marker','Arrow'], annotate=True,figax=(fig,ax) )

### Plotting all the shots of player 9

player9_events = home_events[home_events.From=='Player9']
player9_shots = player9_events[player9_events.Type=='SHOT']

fig,ax = mviz.plot_pitch()
ax.plot( events.loc[1118]['Start X'], events.loc[1118]['Start Y'], 'ro' )
ax.annotate("", xy=events.loc[1118][['End X','End Y']], xytext=events.loc[1118][['Start X','Start Y']], alpha=0.6, arrowprops=dict(arrowstyle="->",color='g'))
ax.plot( events.loc[1681]['Start X'], events.loc[1681]['Start Y'], 'ro' )
ax.annotate("", xy=events.loc[1681][['End X','End Y']], xytext=events.loc[1681][['Start X','Start Y']], alpha=0.6, arrowprops=dict(arrowstyle="->",color='r'))
ax.plot( events.loc[1756]['Start X'], events.loc[1756]['Start Y'], 'ro' )
ax.annotate("", xy=events.loc[1756][['End X','End Y']], xytext=events.loc[1756][['Start X','Start Y']], alpha=0.6, arrowprops=dict(arrowstyle="->",color='r'))
ax.plot( events.loc[1927]['Start X'], events.loc[1927]['Start Y'], 'ro' )
ax.annotate("", xy=events.loc[1927][['End X','End Y']], xytext=events.loc[1927][['Start X','Start Y']], alpha=0.6, arrowprops=dict(arrowstyle="->",color='r'))

## Position of playerswhile player 9socring goal

tracking_home = mio.tracking_data(DATADIR,game_id,'Home')
tracking_away = mio.tracking_data(DATADIR,game_id,'Away')
tracking_home = mio.to_metric_coordinates(tracking_home)
tracking_away = mio.to_metric_coordinates(tracking_away)

fig,ax = mviz.plot_events( events.loc[1118:1118], indicators = ['Marker','Arrow'])
goal_frame = events.loc[1118]['Start Frame']
fig,ax = mviz.plot_frame( tracking_home.loc[goal_frame], tracking_away.loc[goal_frame], figax = (fig,ax) )
