#from flatten_json import flatten
#import pandas as pd
#
#def get_event_data(resp, event_num):
#
#    keys = ['type','event','eventType','description','rbi']
#    flat_df = pd.json_normalize(flatten(resp['liveData']['plays']['allPlays'][event_num]['result']))
#    result_table = flat_df[flat_df.columns.intersection(keys)]
#
#    keys = ['atBatIndex','isTopInning','inning','isScoringPlay','hasReview','hasOut']
#    flat_df = pd.json_normalize(flatten(resp['liveData']['plays']['allPlays'][event_num]['about']))
#    about_table = flat_df[flat_df.columns.intersection(keys)]
#
#    keys = ['batter_id','batter_fullName','batSide_code','batSide_description','pitcher_id','pitcher_fullName','pitchHand_code','pitchHand_description','splits_batter','splits_pitcher','splits_menOnBase']
#    flat_df = pd.json_normalize(flatten(resp['liveData']['plays']['allPlays'][event_num]['matchup']))
#    matchup_table = flat_df[flat_df.columns.intersection(keys)]
#
#    keys = ['count_balls','count_strikes','count_outs','pitchNumber','hitData_launchSpeed','hitData_launchAngle','hitData_totalDistance','hitData_trajectory','hitData_hardness','hitData_location','pitchData_startSpeed','details_call_code']
#    flat_df = pd.json_normalize(flatten(resp['liveData']['plays']['allPlays'][event_num]['playEvents'][-1]))
#    playEvent_table = flat_df[flat_df.columns.intersection(keys)]
#
#    df = pd.concat([result_table, about_table], axis=1)
#
#    df = pd.concat([df, matchup_table], axis=1)
#    df = pd.concat([df, playEvent_table], axis=1)
#
#    return df