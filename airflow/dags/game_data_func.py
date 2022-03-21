#from flatten_json import flatten
#import pandas as pd
#
#def get_game_data(resp):
#    keys = ['condition', 'temp','wind']
#    weather_table = pd.DataFrame.from_dict(flatten(resp['gameData']['weather']), orient='index').T[keys].rename(columns={'condition':'weather'})
#
#    keys = ['id']
#    venue_table = pd.DataFrame.from_dict(flatten(resp['gameData']['venue']), orient='index').T[keys].rename(columns={'id':'park_id'})
#
#    keys = ['pk','type','doubleHeader','season']
#    game_table = pd.DataFrame.from_dict(flatten(resp['gameData']['game']), orient='index').T[keys].rename(columns={'pk':'game_id','type':'game_type','doubleHeader':'double_header'})
#
#    keys = ['away_id','away_fileCode','home_id','home_fileCode']
#    teams_table = pd.DataFrame.from_dict(flatten(resp['gameData']['teams']), orient='index').T[keys].rename(columns={'away_id':'v_tm_id','away_fileCode':'v_tm','home_id':'h_tm_id', 'home_fileCode':'h_tm'})
#
#    df = pd.concat([weather_table, venue_table], axis=1)
#    df = pd.concat([df, game_table], axis=1)
#    df = pd.concat([df, teams_table], axis=1)
#    return df
