"""
Building model for clustersting
"""
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from yellowbrick.cluster import SilhouetteVisualizer
import pickle
import pandas as pd 

def to_feature_df(audio_features_df):
    '''
    Strip audio_features_df of unessecary columns
    '''
    X = audio_features_df[['danceability', 'energy', 'key', 'loudness', 'mode',
       'speechiness', 'acousticness', 'instrumentalness', 'liveness',
       'valence', 'tempo',
       'time_signature']]
    return X


def fit_scaler(X):
    '''
    fit scaler on X-Dataframe. Pickled and return scaler.
    '''
    scaler = StandardScaler()
    scaler.fit(X)
    
    with open("model/scaler.pickle", "wb") as f:
        pickle.dump(scaler,f)


def scale(X):
    '''
    Scale Data of X-Dataframe by using pickled scaler.
    '''
    try:
        with open('model/scaler.pickle', "rb") as f: 
            scaler = pickle.load(f) 
    except FileNotFoundError: 
        print("Scaler not found! Pls fit scaler")

    X_scaled = scaler.transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns = X.columns)

    #display(X.head())
    #display(X_scaled_df.head())
    return X_scaled_df

def train_kmeans(X_scaled_df,number_clusters=25):
    '''
    Train model on X-Dataframe. Pickled and return model.
    '''
    kmeans = KMeans(n_clusters = number_clusters, random_state=42)
    kmeans.fit(X_scaled_df)
    filename = "model/kmeans_" + str(number_clusters) + ".pickle"
    with open(filename, "wb") as f:
        pickle.dump(kmeans,f)
    return kmeans

def load_kmeans(number_clusters=7):
    filename = "model/kmeans_" + str(number_clusters) + ".pickle"
    with open(filename, "rb") as f:
        kmeans = pickle.load(f)
    return kmeans

def give_cluster(X , model):
    return model.predict(scale(X))