import pandas as pd
import datetime
import os
import random
import string
import shortuuid

alphabet = string.ascii_lowercase + string.digits

class match: 
    def __init__(self, match_id, date, set):
        self.match_id = match_id
        self.date = date
        pass

class set: 
    def __init__(self, set_id, venue,  date, players, score):
        self.date = date
        self.venue = venue
        self.players = players
        self.score = score
    def sprint(self):
        print("%2s %2s %2s %2s ".format('Date', 'Venue', 'Players', 'score'))
        print(self.date, ' ', self.venue, ' ', self.players, ' ', self.score)

def extract_games(matches_list: pd.DataFrame, data: pd.DataFrame): 
    games_row = filter_games_row(matches_list, data)
    # print(matches_list)
    for i in range(len(matches_list)):
        date = matches_list.iloc[i]['WinnerFH']
        location = str(matches_list.iloc[i]['WinnerBH'])
        if i != len(matches_list)-1:
            start_index = matches_list.index[i]
            end_index = int(start_index+matches_list.iloc[i+1]['WinScore'])-1
            games_row.loc[start_index:end_index, 'Date'] = date
            games_row.loc[start_index:end_index, 'Location'] = location
        elif i == len(matches_list)-1:
            start_index = matches_list.index[i]
            end_index = int(start_index+5)-1
            games_row.loc[start_index:end_index, 'Date'] = date
            games_row.loc[start_index:end_index, 'Location'] = location
    return games_row

def filter_games_row(matches_list: pd.DataFrame, data: pd.DataFrame):

    def check_type(x):
        try: 
            return type(eval(x)) 
        except Exception as e:
            return type(x)

    games_row = data
    # filter out the unrelated rows 
    games_row = games_row.drop(matches_list.index, errors='ignore')
    typed_rows = games_row.map(check_type)
    condition = (typed_rows['WinnerFH'] == str) & (typed_rows['WinnerBH'] == str) \
                        & (typed_rows['WinScore'] == int) & (typed_rows['LoseScore'] == int) \
                                & (typed_rows['LoserFH'] == str) & (typed_rows['LoserBH'] == str) 
    games_row = games_row[condition]
    return games_row

def extract_match_scores(matches_list: pd.DataFrame, data: pd.DataFrame):
    matches_list.loc[:,'WinScore'] = matches_list.index.diff()
    result = extract_games(matches_list, data)
    return result 

def reindex(data: pd.DataFrame):
    data['MatchID'] = None
    data['GameID'] = None
    for i in range(len(data)):
        data.iat[i,8] = shortuuid.uuid(name=str(data.iloc[i,6].date()))
        data.iat[i,9] = shortuuid.uuid()
    return data 

def multiindex(data: pd.DataFrame):
    return data.set_index(['MatchID', 'GameID'], drop=True)
            
if __name__ == "__main__":
    df = pd.read_excel('Pussy League 2024.xlsx', sheet_name='Cumulative Data')
    df_cl = df.drop(['Winners', 'Losers', 'Unnamed: 8', 0], axis=1)
    df_cl = df_cl.rename(columns={ 'Date': 'WinnerFH', 'Location': 'WinnerBH', 'Unnamed: 4': 'WinScore', 'Unnamed: 5':'LoseScore', 'Unnamed: 6': 'LoserFH', 'Unnamed: 7': 'LoserBH'} )
    tmp_date = pd.to_datetime(df_cl['WinnerFH'], errors='coerce')
    matches_date_location_row = df_cl[tmp_date.notna()]
    matches = extract_match_scores(matches_date_location_row, df_cl)
    matches = reindex(matches)
    matches = multiindex(matches)
    j_matches = matches.to_json('Matches_until_May20_index.json', orient='index')
    j_matches = matches.to_json('Matches_until_May20.json', orient='table')
    # print(j_matches)
    # from json import loads, dumps
    # parsed = loads(j_matches)
    # dumps(parsed, indent=4)
    # print(matches)
'''
Observed Rules: 
ScoreBoard -
Winner (FH) Winner (BH) | [WinScore, LoseScore] | Loser(FH) Loser(BH)

Set : 
    Type : dual
    Players: 
        Winners: 
            (FH): DT
            (BH): WM 
        Losers:
            (FH): Mike 
            (BH): Batty
    Scores:
        Win: 6
        Loss: 3

Request : optimized for adaptive import      
dedup function
'''