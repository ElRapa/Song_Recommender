"""
Spotify Handling
"""
import spotipy
import json
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from helper_functions import chunks_list

# Import API-credentials
import secrets

#Initialize SpotiPy with user credentias
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= secrets.Client_ID,
                                                           client_secret= secrets.Client_Secret))
# top 10000 of all time
# https://open.spotify.com/playlist/1G8IpkZKobrIlXcVPoSIuf

def search_artists_songs(list_artists, lim = 50):
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
    for artist in list_artists:
        results = sp.search(q=artist, limit = lim ,type = 'track', market="GB")['tracks']['items']
        for item in results:
            list_songs.append(item['id'])
    return list_songs

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
    for chunk in list_chunked:
        audio_ft_list = sp.audio_features(chunk)
        song_info_list = sp.tracks(chunk)['tracks']
        for song in range(len(audio_ft_list)):
            song_info = {
                        'artists': [song_info_list[song]['artists'][0]['name']],
                        'name': [song_info_list[song]['name']]
                        }
            audio_ft_song = { key: [audio_ft_list[song][key]] for key in list(audio_ft_list[song].keys()) }
            df = df.append(pd.DataFrame({**song_info, **audio_ft_song}))
    return df