import requests
import json
import pandas as pd
import copy
from tqdm import tqdm

url = "https://api-football-v1.p.rapidapi.com/v3/"
api_host = "api-football-v1.p.rapidapi.com"
api_key = "8759f3b6fbmsh71b1810b860900bp1937a4jsnd81985dca936"
headers = {
        "X-RapidAPI-Host": api_host,
        "X-RapidAPI-Key": api_key
    }
league_ids = {"england" : 39, "spain" : 140, "france" : 61, "italy" : 135,
"germany" : 78}


class League: #league 관련 정보 객체
    def __init__(self, league, season): #league:string, season:string
        self.league = league
        self.season = season
        self.querystring = {"league":league_ids[self.league], "season":self.season}

    def team_list(self): #team_name:team_id 형태의 dict return
        
        response = requests.request("GET", url+"teams", headers=headers, params=self.querystring)
        
        if response.status_code == 200: #응답코드 200: 정상
            response_json = response.json()
            with open(f'data/json/league/team/{self.season}_{self.league}_teams.json', 'w') as f: #JSON 파일 저장
                json_data = json.dump(response_json, f, indent=2)
            team_id_dict = {}
            
            for team in response_json['response']:
                team_id_dict[team['team']['name']]=team['team']['id']

            return team_id_dict
        else:
            print("response failed")
    

    def player_list(self):        
        response = requests.request("GET", url+"players", headers=headers, params=self.querystring)
        
        if response.status_code == 200: #응답코드 200: 정상
            response_json = response.json()
            with open(f'data/json/league/player/{self.season}_{self.league}_players.json', 'w') as f: #JSON 파일 저장
                json_data = json.dump(response_json, f, indent=2)
            player_id_dict = {}
            
            for player in response_json['response']:
                player_id_dict[player['player']['name']]=player['player']['id']

            return player_id_dict
        else:
            print("response failed")

class Team:
    def __init__(self, team_id, team_name, season):
        self.team_id = team_id
        self.season = season
        self.team_name = team_name
        self.querystring = {"team":self.team_id, "season":self.season}

    def player_list(self):
        response = requests.request("GET", url+"players", headers=headers, params=self.querystring)
        
        if response.status_code == 200: #응답코드 200: 정상
            response_json = response.json()
            with open(f'data/json/team/{self.season}_{self.team_name}_players.json', 'w') as f: #JSON 파일 저장
                json_data = json.dump(response_json, f, indent=2)
            player_id_dict = {}
            
            for player in response_json['response']:
                player_id_dict[player['player']['name']]=player['player']['id']
            
            self.player_id_dict = player_id_dict
            self.player_json = response_json
            return player_id_dict
        else:
            print("response failed")


def player_json_to_df(path):
    with open(f'data/json/team/{path}_players.json') as f:
        data = json.load(f)

    data = data['response']
    column_names = []
    for column in data[0]['player'].keys():
        if type(data[0]['player'][column]) == dict:
            for key in data[0]['player'][column].keys():
                column_names.append(f'{column}_{key}')
        else:
            column_names.append(column)
    
    for column in data[0]['statistics'][0].keys():
        if type(data[0]['statistics'][0][column]) == dict:
            for key in data[0]['statistics'][0][column].keys():
                column_names.append(f'{column}_{key}')
        else:
            column_names.append(column)

    dataframe = pd.DataFrame(columns=column_names)
    row = 0

    for player in tqdm(data):
        player_data = []
        for column in player['player'].keys():
            if type(player['player'][column]) == dict:
                for key in player['player'][column].keys():
                    player_data.append(player['player'][column][key])
            else:
                player_data.append(player['player'][column])
        
        for stat in player['statistics']:
            stat_data = copy.deepcopy(player_data)
            for column in stat.keys():
                if type(stat[column]) == dict:
                    for key in stat[column].keys():
                        stat_data.append(stat[column][key])
                else:
                    stat_data.append(stat[column])
            dataframe.loc[row] = stat_data
            row += 1
            
    return dataframe