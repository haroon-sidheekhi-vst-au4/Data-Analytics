# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 13:11:36 2023

data : https://github.com/metrica-sports/sample-data

@author: hp
"""

import Metrica_IO as mio
import Metrica_Viz as mviz

DATADIR = 'E:/Docs/Data/metrica sports sample-data-master/data'
game_id = 2 # let's look at sample match 2

########################    event data loading
events = mio.read_event_data(DATADIR,game_id)
events = mio.to_metric_coordinates(events)

home_events = events[events['Team']=='Home']
away_events = events[events['Team']=='Away']

shots = events[events['Type']=='SHOT']
home_shots = home_events[home_events.Type=='SHOT']
away_shots = away_events[away_events.Type=='SHOT']

home_goals = home_shots[home_shots['Subtype'].str.contains('-GOAL')].copy()
away_goals = away_shots[away_shots['Subtype'].str.contains('-GOAL')].copy()

########################    tracking data loading
tracking_home = mio.tracking_data(DATADIR,game_id,'Home')
tracking_away = mio.tracking_data(DATADIR,game_id,'Away')

tracking_home = mio.to_metric_coordinates(tracking_home)
tracking_away = mio.to_metric_coordinates(tracking_away)

############## reversing the diagnol
tracking_home,tracking_away,events = mio.to_single_playing_direction(tracking_home,tracking_away,events)

#######################     plot passes to goal
fig,ax = mviz.plot_pitch()
ax.plot( events.loc[198]['Start X'], events.loc[198]['Start Y'], 'ro' )
ax.annotate("", xy=events.loc[198][['End X','End Y']], xytext=events.loc[198][['Start X','Start Y']], alpha=0.6, arrowprops=dict(arrowstyle="->",color='r'))

#190:198
#819:823
mviz.plot_events( events.loc[190:198], indicators = ['Marker','Arrow'], annotate=True )

######################      plotting player movements

fig,ax = mviz.plot_pitch()
ax.plot( tracking_home['Home_11_x'].iloc[:1000], tracking_home['Home_11_y'].iloc[:1000], 'r.', ms=1)
ax.plot( tracking_home['Home_1_x'].iloc[:1000], tracking_home['Home_1_y'].iloc[:1000], 'b.', ms=1)
ax.plot( tracking_home['Home_2_x'].iloc[:1000], tracking_home['Home_2_y'].iloc[:1000], 'g.', ms=1)
ax.plot( tracking_home['Home_3_x'].iloc[:1000], tracking_home['Home_3_y'].iloc[:1000], 'k.', ms=1)
ax.plot( tracking_home['Home_4_x'].iloc[:1000], tracking_home['Home_4_y'].iloc[:1000], 'c.', ms=1)

fig,ax = mviz.plot_pitch()
ax.plot( tracking_home['Home_11_x'].iloc[:141156], tracking_home['Home_11_y'].iloc[:141156], 'r.', ms=1)

fig,ax = mviz.plot_pitch()
ax.plot( tracking_home['Home_1_x'].iloc[:141156], tracking_home['Home_1_y'].iloc[:141156], 'b.', ms=1)

fig,ax = mviz.plot_pitch()
ax.plot( tracking_home['Home_2_x'].iloc[:141156], tracking_home['Home_2_y'].iloc[:141156], 'g.', ms=1)

fig,ax = mviz.plot_pitch()
ax.plot( tracking_home['Home_3_x'].iloc[:141156], tracking_home['Home_3_y'].iloc[:141156], 'k.', ms=1)

fig,ax = mviz.plot_pitch()
ax.plot( tracking_home['Home_4_x'].iloc[:141156], tracking_home['Home_4_y'].iloc[:141156], 'c.', ms=1)

#Positions while finsihing the match
KO_Frame = events.loc[1934]['Start Frame']
fig,ax = mviz.plot_frame( tracking_home.loc[KO_Frame], tracking_away.loc[KO_Frame] )

#Positions during GOAL
fig,ax = mviz.plot_events( events.loc[823:823], indicators = ['Marker','Arrow'], annotate=True )
goal_frame = events.loc[823]['Start Frame']
fig,ax = mviz.plot_frame( tracking_home.loc[goal_frame], tracking_away.loc[goal_frame], figax = (fig,ax) )

