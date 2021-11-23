#Import Libraries
print('Line 2')
import pandas as pd
import requests
from bs4 import BeautifulSoup

print('Line 6')

# Define function to scrape data from website
def scrape_top100():
    ### 2.1 Get and parse data from billboard.com 
    url = 'https://www.billboard.com/charts/hot-100/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    ### 2.2 Scrape raw list of songs and artist
    list_song_raw = soup.select('.o-chart-results-list__item .c-title')
    list_song = []
    list_artist_raw = soup.select('.o-chart-results-list__item .c-label.a-no-trucate')
    list_artist = []
    ### 2.3 Clean strings and save to list
    for n in list_artist_raw:
        list_artist.append(n.get_text()[1:-1])
    len(list_artist)
    for n in list_song_raw:
        list_song.append(n.get_text()[1:-1])
    len(list_song)
    ### 2.4 Merge song- and artist-list to DataFrame
    df = pd.DataFrame({'song':list_song,'artist':list_artist})
    return df


# Define function to recommend song
def recommend_song():
    '''
    recommend_song(Empty)
    Function will ask for song and checks if its in df.
    Input: 
    Output: Print recommendation
    '''
    song = input('What song do you want a recommendation for? ')
    df = scrape_top100()
    if song not in list(df.song):
        print('Möp.',song,'is not in the Top100!')
    else:
        recommendation = df.sample()
        print('Hot Tune! What about "'+ recommendation.iloc[0,0]+'" by "'+ recommendation.iloc[0,1]+'"?')

recommend_song()