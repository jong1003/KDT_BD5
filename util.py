import os
import pandas as pd
from tqdm import tqdm


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
    
