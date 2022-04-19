import json
import dataloder
import pandas as pd

df = dataloder.json_to_df('2021_40_players')
df.to_csv('data/csv/team/liverpool.csv')