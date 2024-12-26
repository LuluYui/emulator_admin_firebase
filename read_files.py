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

# Extracting the game scores into the matches_list table
def extract_games(matches_list: pd.DataFrame, data: pd.DataFrame): 
    games_row = filter_games_row(matches_list, data)
    
     # Add 'Date' and 'Location' columns if they don't exist
    if 'Date' not in games_row.columns:
        games_row['Date'] = None
    if 'Location' not in games_row.columns:
        games_row['Location'] = None

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

    score_columns = ['WinScore', 'LoseScore']
    games_row = data
    # remove all the rows with date and location value 
    games_row = games_row.drop(matches_list.index, errors='ignore')
    # remove all the rows without winscore and losescore
    games_row[score_columns] = games_row[score_columns].apply(pd.to_numeric, errors='coerce')
    games_row = games_row.dropna(subset=['WinScore', 'LoseScore'])
    # Make sure the type of the integer columns as integers
    games_row[score_columns] = games_row[score_columns].astype(int)
    
    typed_rows = games_row.map(check_type)
    # check if the game scores are int typed 
    
    condition = (typed_rows['WinnerFH'] == str) & (typed_rows['WinnerBH'] == str) \
                        & (typed_rows['WinScore'] == int) & (typed_rows['LoseScore'] == int) \
                                & (typed_rows['LoserFH'] == str) & (typed_rows['LoserBH'] == str) 
    games_row = games_row[condition]
    return games_row

def extract_match_scores(matches_list: pd.DataFrame, data: pd.DataFrame):
    matches_list.loc[:,'WinScore'] = matches_list.index.diff()
    result = extract_games(matches_list, data)
    return result 

# Tag every matches and games with specific UUIDs on columns 8 and 9
def reindex(data: pd.DataFrame):
    data['MatchID'] = None
    data['GameID'] = None
    for i in range(len(data)):
        data.iat[i,8] = shortuuid.uuid(name=str(data['Date']))
        data.iat[i,9] = shortuuid.uuid()
    # Rename the columns of UUIDs 
    data = data.rename(columns={
                                data.columns[8]: 'gamesUUID', 
                                data.columns[9]: 'matchesUUID',
                                })
    return data 

def multiindex(data: pd.DataFrame):
    return data.set_index(['MatchID', 'GameID'], drop=True)
            
# Structure the messy matches table into a row structure
# such that a dataframe headers will result as : 
# INDEX DATE WINNERFH WINNERBH WINSCORE LOSESCRORE LOSERFH LOSERBH 
def massage_data(sheet_name = 'Cumulative Data'):
    df = pd.read_excel('./data/Pussy League 2024.xlsx', sheet_name=sheet_name)
    df_cl = df.drop(['Winners', 'Losers', 'Unnamed: 8', 0], axis=1)
    df_cl = df_cl.rename(columns={ 'Date': 'WinnerFH', 'Location': 'WinnerBH', 'Unnamed: 4': 'WinScore', 'Unnamed: 5':'LoseScore', 'Unnamed: 6': 'LoserFH', 'Unnamed: 7': 'LoserBH'} )
    tmp_date = pd.to_datetime(df_cl['WinnerFH'], errors='coerce')
    matches_date_location_row = df_cl[tmp_date.notna()]

    # Extract the matches from the date and location, 
    # then organize them into a tabular rows of matches
    # Input1 ( matches_date_location_row ) : the date location listed for filling in the matches scores
    # Input2 ( df_cl ) : the original matches table with all the data 
    matches = extract_match_scores(matches_date_location_row, df_cl)
    matches = reindex(matches)
    matches = multiindex(matches)
    j_matches = matches.to_json('./data/Matches_until_may20.json', orient='table')

def massage_rollingdata(sheet_name = 'Rolling Data'):
    df = pd.read_excel('./data/Pussy League 2024.xlsx', sheet_name=sheet_name)
    df_cl = df.rename(columns={ 7: 'WinnerFH', 'Unnamed: 3': 'WinnerBH', 'Unnamed: 4': 'WinScore', 'Unnamed: 5':'LoseScore', 'Unnamed: 6': 'LoserFH', 'Unnamed: 7': 'LoserBH'} )
    tmp_date = pd.to_datetime(df_cl['WinnerFH'], errors='coerce')
    matches_date_location_row = df_cl[tmp_date.notna()]
    matches = extract_match_scores(matches_date_location_row, df_cl)
    matches = reindex(matches)
    matches = multiindex(matches)
    j_matches = matches.to_json('./data/Matches_rollingdata.json', orient='table')

if __name__ == "__main__":
    # reading cumulative data page 
    # massage_rollingdata()
    massage_data()
    
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