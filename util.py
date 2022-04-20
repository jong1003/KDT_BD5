import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

class DataFile:
    def __init__(self, path):
        self.path = path
        self.file_list = os.listdir(path)
        self.counts = len(self.file_list)
    
    def load_csv(self):
        data = pd.read_csv(self.path+self.file_list[0])
        for file in tqdm(self.file_list[1:]):
            data = pd.concat([data, pd.DataFrame(pd.read_csv(self.path+file))])
        return data
    
def heat_map_proportion(data, proportions, position, min_appearance=5, size=25):
    data = data[(data['games_appearences']>=min_appearance)&(data['games_minutes']!=0)&(data['games_position']!=position)]
    data.fillna(0)
    target_data = pd.DataFrame()
    for proportion in proportions:
        target_data[proportion] = data[proportion]/data['games_minutes']
    target_data['games_rating'] = data['games_rating']
    plt.rcParams["figure.figsize"] = (size, size)
    sb.heatmap(target_data.corr(),
           annot = True, #실제 값 화면에 나타내기
           cmap = 'Greens', #색상
           vmin = -1, vmax=1 , #컬러차트 영역 -1 ~ +1
          )


def heat_map_rate(data, rates, position, min_appearance=5, size=25):
    data = data[(data['games_appearences']>=min_appearance)&(data['games_minutes']!=0)&(data['games_position']!=position)]
    data.fillna(0)
    target_data = data[rates]
    target_data['games_rating'] = data['games_rating']
    plt.rcParams["figure.figsize"] = (size, size)
    sb.heatmap(target_data.corr(),
           annot = True, #실제 값 화면에 나타내기
           cmap = 'Greens', #색상
           vmin = -1, vmax=1 , #컬러차트 영역 -1 ~ +1
          )