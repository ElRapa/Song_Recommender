"""
Data Handling
Opening and saving files
txt, csv, etc
"""
import pandas as pd
import pickle

def concat_csvs(filename, amount, path ='data/'):
    '''
    concat multiple csvs with same filename (without csv)
    '''
    df = pd.DataFrame()
    for f in range(amount):
        df = df.append(pd.read_csv(path + filename + '_'+str(f+1)+'.csv')).reset_index(drop=True)
    return df

def compare_song_lists(song_list_update):
    '''
    compare list of songs to update with song_list already scraped (audio_feautures)
    '''
    with open('data/song_id_list.txt','rb') as fp:
        song_list = pickle.load(fp)
    song_list_update = list(set(song_list_update)-set(song_list))
    with open('data/song_id_list_update.txt','wb') as fp:
        pickle.dump(song_list_update,fp)
    len(song_list_update)
    return song_list_update

def update_audiofeatures_csv(df_update):
    df_audiofeautures = pd.read_csv('data/audio_features.csv')
    df_audiofeautures_new = pd.concat([df_audiofeautures,df_update]).reset_index(drop=True)
    df_audiofeautures_new.to_csv('data/audio_features.csv',index=False)  
    print('Finished')
    return df_audiofeautures_new


