import dataloder

def load_season_data(season):
    for league in dataloder.league_ids.keys():
        league_info = dataloder.League(league, season)
        team_list = league_info.team_list()
        for team in team_list.keys():
            team_id = team_list[team]
            team_info = dataloder.Team(team_id, team, season)
            team_info.player_list()
            player_df = dataloder.player_json_to_df(f"{season}_{team}")
            player_df.to_csv(f"data/csv/team/{season}_{team}.csv")

load_season_data("2021")