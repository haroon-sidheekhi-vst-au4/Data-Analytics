# -*- coding: utf-8 -*-
"""
Created on Sat May 27 00:46:08 2023

@author: hp
"""


import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch

from pandas.io.json import json_normalize

import json

with open('E:/Docs/Data/Skill corner/opendata/data/matches.json') as a:
    competitions = json.load(a)
competitions_df = json_normalize(competitions, sep = "_")
#event data

with open('E:/Docs/Data/Skill corner/opendata/data/matches/2068/structured_data.json',encoding='utf-8') as f:
    data = json.load(f)
from pandas.io import json

match_df = json_normalize(data, sep = "_")

