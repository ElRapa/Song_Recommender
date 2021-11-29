"""
Spotify Handling
"""
import spotipy
import json
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from helper_functions import chunks_list
import helper_functions as hf
from tqdm.auto import tqdm

# Import API-credentials
import secrets

#Initialize SpotiPy with user credentias
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= secrets.Client_ID,
                                                           client_secret= secrets.Client_Secret))
# top 10000 of all time
# https://open.spotify.com/playlist/1G8IpkZKobrIlXcVPoSIuf

def search_songs(list_artists, lim = 50):
    '''
    Get song-IDs for a list of strings via spotify search.

    Parameters
    ----------
    list_artists : list
        Terms to search for
    lim : (1:50), default = 50
        Limit of search results per entry
    Returns
    -------
    list_songs: list
        Cumulated list of song IDs for each search term
    '''
    list_songs = []
    for artist in tqdm(list_artists):
        results = sp.search(q=artist, limit = lim ,type = 'track', market="GB")['tracks']['items']
        for item in results:
            list_songs.append(item['id'])
    return list(set(list_songs))

def get_audio_feautures(list_songs):
    '''
    Get DataFrame with song-info and -audiofeatures for a list of song-IDs.

    Parameters
    ----------
    list_songs : list
        Songs to save song-info and -audiofeatures

    Returns
    -------
    Dataframe: 
        columns = ['artists', 'name', 'danceability', 'energy', 'key', 'loudness', 'mode',
       'speechiness', 'acousticness', 'instrumentalness', 'liveness',
       'valence', 'tempo', 'type', 'id', 'uri', 'track_href', 'analysis_url',
       'duration_ms', 'time_signature']        
    '''
    list_chunked = chunks_list(list_songs,50)
    df = pd.DataFrame()
    counter = 0
    error_count_song_info = 0
    error_count_song_features = 0
    error_count_chunks = 0
    ignore_list = []
    for chunk in tqdm(list_chunked):
        counter += 1
        try:    
            audio_ft_list = sp.audio_features(chunk)
            song_info_list = sp.tracks(chunk)['tracks']
            for song in range(len(audio_ft_list)):
                try:
                    if len(song_info_list[song]) >= 0 and len(audio_ft_list[song]) >= 0:
                        song_info = {
                                'artists': [song_info_list[song]['artists'][0]['name']],
                                'song': [song_info_list[song]['name']]
                                }
                        try:
                            audio_ft_song = { key: [audio_ft_list[song][key]] for key in list(audio_ft_list[song].keys()) }
                            df = df.append(pd.DataFrame({**song_info, **audio_ft_song}))
                        except:
                            error_count_song_info += 1
                            try:
                                ignore_list.append(song)                            
                            except:
                               continue
                            continue
                except:
                    error_count_song_features += 1
                    try:
                        ignore_list.append(song)                            
                    except:
                        continue
                    continue
        except:
            error_count_chunks += 1
            continue
    print('Amount of song-info-errors: ', error_count_song_info)
    print('Amount of song-features-errors: ', error_count_song_features)
    print('Amount of chunking-errors: ', error_count_chunks)
    try:
        list_songs = list(set(list_songs-set(ignore_list)))
        print('List of songs has been updated. New song list is not saved/handled')
    except:
        pass
    return df

def save_song_list_to_csv(song_list, start_suffix=1 , path ='data/',filename='audio_features_update_'):
    '''
    Scrape audiofeatures of song list and save to multiple csvs
    Parameters
    ----------
    list_songs : list
        Songs to save song-info and -audiofeatures
    start_suffix : int, default = 1
    path : str, default = 'data/'
    filename: str, default = 'audio_features_update_'

    Returns
    -------
    DataFrame
        songs with audiofeatures
    DF saved to multiple csvs
    '''
    list_chunked = hf.chunks_list(song_list,10000)
    for chunk in tqdm(list_chunked):
        df_audiofeatures = get_audio_feautures(chunk)
        df_audiofeatures.to_csv(path+filename+str(start_suffix)+'.csv',index=False)
        start_suffix += 1
    print('Finished')
    print('counter:', str(start_suffix))
    return df_audiofeatures

def results_to_txt(list,path):
    hf.write_list_txt(list,path)
    return

def results_from_txt(path):
    return hf.read_list_txt(path)

def play(track_id):
    from IPython.display import IFrame
    IFrame(src=f"https://open.spotify.com/embed/track/{track_id}",
        width="320",
        height="80",
        frameborder="0",
        allowtransparency="true",
        allow="encrypted-media",
        )