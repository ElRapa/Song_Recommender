from scraping import load_or_scrape

# Define function to recommend song

def recommend_hot100():
    '''
    recommend_song(Empty)
    Function will ask for song and checks if its in df.
    Input: 
    Output: Print recommendation
    '''
    song = input('What song do you want a recommendation for? ').str.lower()
    df = load_or_scrape('billboard100')
    if song not in list(df.song.str.lower()):
        print('Möp.',song,'is not in the Top100!')
    else:
        recommendation = df.sample()
        print('Hot Tune! What about "'+ recommendation.iloc[0,0]+'" by "'+ recommendation.iloc[0,1]+'"?')


def ask_if_correct_song(song, df):
    df_column = df['song'].str.lower()
    song = song.lower() 
    if song in list(df_column):
        songs_found = len(df[df_column == song])
        for i in range(songs_found):
            artist = df[df_column == song].iloc[0]['artists']
            song_db = df[df_column == song].iloc[0]['song']
            user_input = ''
            while user_input not in ['yes','no']:
                user_input = input(("Did you mean '" +song_db+ "' by '" +artist+ "'? Type yes or no"))
            if user_input == 'yes':
                print("Oh, that's a nice one!")
                df = df[df_column == song]
                return df
            else:
                print('song not in Database')
    else:
        print(song, 'not in Database')
    return df

def recommend_af(song_af,df_audiofeatures,k=50,recommendations=10): #29
    '''
    Recommendation based on audiofeatures
    '''
    from modelling import load_kmeans, scale, train_kmeans, to_feature_df
    # scale x
    X_scaled = scale(to_feature_df(df_audiofeatures))
    song_scaled = scale(to_feature_df(song_af))
    try:
        kmeans = load_kmeans(number_clusters=k)
    except:
        kmeans = train_kmeans(X_scaled, number_clusters=k)

    clusters = kmeans.predict(X_scaled)
    df_audiofeatures['cluster'] = clusters

    song_cluster = kmeans.predict(song_scaled)[0]

    return df_audiofeatures[df_audiofeatures['cluster'] == song_cluster].sample(recommendations).drop(columns=['cluster'])


def recommend():
    '''
    Recommendation based on hotness if not, then: audiofeatures
    '''

    import pandas as pd
    from spotifyhandler import play

    hot100 = pd.read_csv('data/billboard_top100.csv')
    df_audiofeatures = pd.read_csv('data/audio_features.csv')
    song = input(("Give it to me baby! Give me a song: ")).lower()
    df_combined = df_audiofeatures.append(hot100)
    #song_af = ask_if_correct_song(song,df_audiofeatures)
    song_af = ask_if_correct_song(song,df_combined)
    song_af = df_audiofeatures.loc[song_af.index]
    recommendation = 'Sorry no recommendation'
    if song in list(hot100['song'].str.lower()):
        recommendation = hot100.sample()
        print('Hot Tune! What about "'+ recommendation.iloc[0,0]+'" by "'+ recommendation.iloc[0,1]+'"?')
        return
    elif song in list(df_audiofeatures['song'].str.lower()):
        try:
            recommendation_df = recommend_af(song_af,df_audiofeatures)
            user_input = 'no'
            n = 0
            while user_input != 'yes' and n<=len(recommendation_df):
                artist = recommendation_df.iloc[n]['artists']
                song_db = recommendation_df.iloc[n]['song']
                user_input = input(("Maybe you'll like '" +song_db+ "' by '" +artist+ "'? Type yes or no"))
                n +=1
            return recommendation_df.iloc[n-1]['id']
            
        except:
            print('Something went wrong with getting the song audio features')
    else:
        print('Song not found')
    return recommendation


def recommender_test():
    '''
    Recommendation based on hotness if not, then: audiofeatures
    '''


    import pandas as pd
    from spotifyhandler import play
    from IPython.display import IFrame


    hot100 = pd.read_csv('data/billboard_top100.csv')
    df_audiofeatures = pd.read_csv('data/audio_features.csv')
    song = input(("Give it to me baby! Give me a song: ")).lower()
    df_combined = df_audiofeatures.append(hot100)
    #song_af = ask_if_correct_song(song,df_audiofeatures)
    song_af = ask_if_correct_song(song,df_combined)
    song_af = df_audiofeatures.loc[song_af.index]
    recommendation = 'Sorry no recommendation'
    if song in list(hot100['song'].str.lower()):
        recommendation = hot100.sample()
        print('Hot Tune! What about "'+ recommendation.iloc[0,0]+'" by "'+ recommendation.iloc[0,1]+'"?')
        return
    elif song in list(df_audiofeatures['song'].str.lower()):
        try:
            recommendation_df = recommend_af(song_af,df_audiofeatures)
            user_input = 'no'
            n = 0
            while user_input != 'yes' and n<=len(recommendation_df):
                artist = recommendation_df.iloc[n]['artists']
                song_db = recommendation_df.iloc[n]['song']
                id = recommendation_df.iloc[n-1]['id']
                yield IFrame(src=f"https://open.spotify.com/embed/track/{track_id}",
                            width="320",
                            height="80",
                            frameborder="0",
                            allowtransparency="true",
                            allow="encrypted-media",
                            )
                user_input = input(("Maybe you'll like '" +song_db+ "' by '" +artist+ "'? Type yes or no: "))
                n +=1
            return recommendation_df.iloc[n-1]['id']
            
        except:
            print('Something went wrong with getting the song audio features')
    else:
        print('Song not found')
    return recommendation

def get_similar_song(song, df):
    if song in df['name']:
        print(song)
