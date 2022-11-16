# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 19:48:48 2022

@author: dev
"""

#importing necessary libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mplsoccer import Sbopen, Pitch
import statsmodels.api as sm
import statsmodels.formula.api as smf
from matplotlib import colors
import json
from pandas import json_normalize
import parser
parser = Sbopen()

competition_id=72
season_id=30
with open('E:/SoccermaticsForPython-master/statsbomb/data/matches/'+str(competition_id)+'/'+str(season_id)+'.json') as d1:
    matches = json.load(d1)    
df_match = json_normalize(matches, sep = "_")

#get names of all teams
teams = df_match["home_team_home_team_name"].unique()
#get indicies of all games
match_ids = df_match["match_id"]

#empty dataframes
passshot_df = pd.DataFrame()
danger_passes_df = pd.DataFrame()
#for every game in the tournament
for idx in match_ids:
    #open event data
    with open('E:/SoccermaticsForPython-master/statsbomb/data/events/'+str(idx)+'.json') as f:
        datas = json.load(f)
        df = json_normalize(datas, sep = "_")
    #get home and away team
    home_team = df_match.loc[df_match["match_id"] == idx]["home_team_home_team_name"].iloc[0]
    away_team = df_match.loc[df_match["match_id"] == idx]["away_team_away_team_name"].iloc[0]
    #for both teams
    for team in [home_team, away_team]:
        #declare variables to sum shots, passes and danger passes from both halves
        shots = 0
        passes = 0
        danger_passes = 0
        #for both periods - see previous lessons
        for period in [1, 2]:
            #passes
            df.info()
            mask_pass = (df.team_name == team) & (df.type_name == "Pass") & (df.pass_outcome_name.isnull()) & (df.period == period)
            pass_df = df.loc[mask_pass]
            #A dataframe of shots
            mask_shot = (df.team_name == team) & (df.type_name == "Shot") & (df.period == period)
            #Find passes within 15 seconds of a shot, exclude corners.
            shot_df = df.loc[mask_shot, ["minute", "second"]]
            #convert time to seconds
            shot_times = shot_df['minute']*60+shot_df['second']
            shot_window = 15
            #find starts of the window
            shot_start = shot_times - shot_window
            #condition to avoid negative shot starts
            shot_start = shot_start.apply(lambda i: i if i>0 else (period-1)*45)
            #convert to seconds
            pass_times = pass_df['minute']*60+pass_df['second']
            #check if pass is in any of the windows for this half
            pass_to_shot = pass_times.apply(lambda x: True in ((shot_start < x) & (x < shot_times)).unique())
            danger_passes_period = pass_df.loc[pass_to_shot]

            #will need later all danger passes
            danger_passes_df = pd.concat([danger_passes_df, danger_passes_period])

            #adding number of passes, shots and danger passes from a game
            passes += len(pass_df)
            shots += len(shot_df)
            danger_passes += len(danger_passes_period)
        #getting number of goals by the team from the game
        if team == home_team:
            goals = df_match.loc[df_match["match_id"] == idx]["home_score"].iloc[0]
        else:
            goals = df_match.loc[df_match["match_id"] == idx]["away_score"].iloc[0]
        #appending passshot dataframe
        match_info_df = pd.DataFrame({
                    "Team": [team],
                    "Passes": [passes],
                    "Shots": [shots],
                    "Goals": [goals],
                    "Danger Passes": [danger_passes]
                    })
        passshot_df = pd.concat([passshot_df, match_info_df])
        
fig, ax = plt.subplots()
#plot all games
ax.plot('Passes','Shots', data=passshot_df, linestyle='none', markersize=4, marker='o', color='grey')
#choose only England games and plot them red
england_df  = passshot_df.loc[passshot_df["Team"] == "England Women's"]
ax.plot('Passes','Shots', data=england_df, linestyle='none', markersize=6, marker='o', color='red')
#make legend
ax.set_xticks(np.arange(0,1000,step=100))
ax.set_yticks(np.arange(0,40,step=5))
ax.set_xlabel('Passes (x)')
ax.set_ylabel('Shots (y)')
plt.show()


#repeat plotting points for
fig,ax=plt.subplots()
#plot all games
ax.plot('Passes','Shots', data=passshot_df, linestyle='none', markersize=4, marker='o', color='grey')
#choose only England games and plot them red
england_df  = passshot_df.loc[passshot_df["Team"] == "England Women's"]
ax.plot('Passes','Shots', data=england_df, linestyle='none', markersize=6, marker='o', color='red')
#make legend
ax.set_xticks(np.arange(0,700,step=100))
ax.set_yticks(np.arange(0,40,step=5))
ax.set_xlabel('Passes (x)')
ax.set_ylabel('Shots (y)')

#changing datatype for smf
passshot_df['Shots']= pd.to_numeric(passshot_df['Shots'])
passshot_df['Passes']= pd.to_numeric(passshot_df['Passes'])
passshot_df['Goals']= pd.to_numeric(passshot_df['Goals'])

#fit the model
model_fit=smf.ols(formula='Shots ~ Passes', data=passshot_df[['Shots','Passes']]).fit()
#print summary
print(model_fit.summary())
#get coefficients
b = model_fit.params
#plot line
x = np.arange(0, 1000, step=0.5)
y = b[0] + b[1]*x
ax.plot(x, y, linestyle='-', color='black')
#make legend
ax.set_ylim(0,40)
ax.set_xlim(0,800)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()


fig,ax=plt.subplots()
#plot all games
ax.plot('Passes','Goals', data=passshot_df, linestyle='none', markersize=4, marker='o', color='grey')
#choose only England games and plot them red
england_df  = passshot_df.loc[passshot_df["Team"] == "England Women's"]
ax.plot('Passes','Goals', data=england_df, linestyle='none', markersize=6, marker='o', color='red')
#make legend
ax.set_xticks(np.arange(0,700,step=100))
ax.set_yticks(np.arange(0,13,step=2))
ax.set_xlabel('Passes (x)')
ax.set_ylabel('Goals (y)')

#fit the model
poisson_model = smf.glm(formula="Goals ~ Passes", data=passshot_df,
                    family=sm.families.Poisson()).fit()
#print summary
poisson_model.summary()
#get coefficients
b = poisson_model.params
#plot line
x = np.arange(0, 1000, step=0.5)
y = np.exp(b[0] + b[1]*x)
ax.plot(x, y, linestyle='-', color='black')
#make legend
ax.set_ylim(0,15)
ax.set_xlim(0,550)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()

#plot pitch
pitch = Pitch(line_zorder=2, line_color='black')
fig, axs = pitch.grid(ncols = 6, nrows = 4, figheight=20,
                      grid_width=0.88, left=0.025,
                      endnote_height=0.03, endnote_space=0,
                      axis=False,
                      title_space=0.02, title_height=0.06, grid_height=0.8)

#for each team store  bins in a dictionary
hist_dict = {}
for team in teams:
    #get number of games by team
    no_games = len(df_match.loc[(df_match["home_team_home_team_name"] == team) | (df_match["away_team_away_team_name"] == team)])
    #get danger passes only by this team
    team_danger_passes = danger_passes_df.loc[danger_passes_df["team_name"] == team]
    #number of danger passes in each zone
    team_danger_passes["x"] = team_danger_passes["location"].apply(str).str.split(", ", expand=True)[0].str[1:].apply(pd.to_numeric)
    team_danger_passes["y"] = team_danger_passes["location"].apply(str).str.split(", ", expand=True)[1].str[:-1].apply(pd.to_numeric)
    bin_statistic = pitch.bin_statistic(team_danger_passes.x, team_danger_passes.y, statistic='count', bins=(6, 5), normalize=False)
    #normalize by number of games
    bin_statistic["statistic"] = bin_statistic["statistic"]/no_games
    #store in dictionary
    hist_dict[team] = bin_statistic

#calculating average per game per team per zone
avg_hist = np.mean(np.array([v["statistic"] for k,v in hist_dict.items()]), axis=0)

#subtracting average
for team in teams:
    hist_dict[team]["statistic"] = hist_dict[team]["statistic"] - avg_hist

#preparing colormap
vmax = max([np.amax(v["statistic"]) for k,v in hist_dict.items()])
vmin = min([np.amin(v["statistic"]) for k,v in hist_dict.items()])
divnorm = colors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)
#for each player
for team, ax in zip(teams, axs['pitch'].flat):
    #put team name over the plot
    ax.text(60, -5, team,
            ha='center', va='center', fontsize=24)
    #plot colormap
    pcm  = pitch.heatmap(hist_dict[team], ax=ax, cmap='coolwarm', norm = divnorm, edgecolor='grey')

#make legend
ax_cbar = fig.add_axes((0.94, 0.093, 0.02, 0.77))
cbar = plt.colorbar(pcm, cax=ax_cbar, ticks=[-1.5, -1, -0.5, 0, 1, 2, 3])
cbar.ax.tick_params(labelsize=30)
ax_cbar.yaxis.set_ticks_position('left')
#add title
axs['title'].text(0.5, 0.5, 'Danger passes per game - performance above zone average', ha='center', va='center', fontsize=60)
plt.show()
