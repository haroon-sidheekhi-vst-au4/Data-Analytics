# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 18:33:17 2021

@author: dev
"""

import json
print('hello')
with open('E:\SoccermaticsForPython-master\statsbomb\data\competitions.json') as f:
    competitions = json.load(f)
    
competition_id=43
with open('E:/SoccermaticsForPython-master/statsbomb/data/matches/'+str(competition_id)+'/3.json') as f:
    matches = json.load(f)  
    
for match in matches:
    first_team = match['home_team']['home_team_name']
    second_team = match['away_team']['away_team_name']
    print (first_team +' playing with ' + second_team)
    
for match in matches:
    x='England'
    y='Belgium'
    if(match['home_team']['home_team_name']==x) and (match['away_team']['away_team_name']==y):
        id = match['match_id']
        print(id)
        
for match in matches:
    if(match['match_id']==7570):
        print(match['stadium']['name'])
        
        
#1, Print out the list for the Mens World cup 

import json
with open('E:\SoccermaticsForPython-master\statsbomb\data\competitions.json') as f:
    competitions = json.load(f)
competition_id=43
with open('E:/SoccermaticsForPython-master/statsbomb/data/matches/'+str(competition_id)+'/3.json') as f:
    matches = json.load(f)  
    
for match in matches:
    home_team_name=match['home_team']['home_team_name']
    away_team_name=match['away_team']['away_team_name']
    home_score=match['home_score']
    away_score=match['away_score']
    describe_text = 'The match between ' + home_team_name + ' and ' + away_team_name
    result_text = ' finished ' + str(home_score) +  ' : ' + str(away_score)
    print(describe_text + result_text)
    
#2, Find the ID for England vs. Sweden
import json
with open('E:\SoccermaticsForPython-master\statsbomb\data\competitions.json') as f:
    competitions = json.load(f)
competition_id=43

with open('E:/SoccermaticsForPython-master/statsbomb/data/matches/'+str(competition_id)+'/3.json') as f:
    matches = json.load(f) 
    
home_team_required ="Sweden"
away_team_required ="England"

#Find ID for the match
for match in matches:
    home_team_name=match['home_team']['home_team_name']
    away_team_name=match['away_team']['away_team_name']
    if (home_team_name==home_team_required) and (away_team_name==away_team_required):
        match_id = match['match_id']
print(home_team_required + ' vs ' + away_team_required + ' has id:' + str(match_id))

#3, Write out a list of just Sweden's results in the tournament.

import json
with open('E:\SoccermaticsForPython-master\statsbomb\data\competitions.json') as f:
    competitions = json.load(f)
competition_id=43

with open('E:/SoccermaticsForPython-master/statsbomb/data/matches/'+str(competition_id)+'/3.json') as f:
    matches = json.load(f) 
    
for match in matches:
    if (match['home_team']['home_team_name']=='Sweden') or (match['away_team']['away_team_name']=='Sweden'):
        home_score=match['home_score']
        away_score=match['away_score']
        result = 'Match between '+match['home_team']['home_team_name']+' and '+match['away_team']['away_team_name']+' resulted in '+str(home_score) +':'+ str(away_score)
        print (result)






