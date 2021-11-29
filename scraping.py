#Import Libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_html(url):
    response = requests.get(url)
    status_code = response.status_code
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup, response, status_code

# Define function to scrape data from website
def scrape_top100(soup):
    '''
    Handle soup (billboard top100) provided and create df with artists and songs
    '''
    ### 2.1 Get and parse data from url billboard.com 
    # moved to scrape html
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
    df = pd.DataFrame({
        'song':list_song,
        'artists':list_artist
        })
    return df

# Scrape inital Page with unique url
def scrape_wiki_artist(soup):
    '''
    Handle soup (wikipedia_artists) provided and create list with artist that have a song-list-page
    '''
    wiki_list_artist = soup.select('body.mediawiki.ltr.sitedir-ltr.mw-hide-empty-elt.ns--1.ns-special.mw-special-Prefixindex.page-Special_PrefixIndex.rootpage-Special_PrefixIndex.skin-vector.action-view.skin-vector-legacy div#content.mw-body div#bodyContent.vector-body div#mw-content-text.mw-body-content div.mw-prefixindex-body ul.mw-prefixindex-list')
    wiki_list_artist = wiki_list_artist[0].get_text()[1:-1].split(sep='\n ')
    last = wiki_list_artist[-1]
    for i in range(20):
        try:
            url = 'https://en.wikipedia.org/w/index.php?title=Special:PrefixIndex&from=List_of_songs_recorded_by_'+last+'_Esp%C3%B3sito&prefix=List+of+songs+recorded+by&stripprefix=1'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            wiki_list_artist_add = soup.select('body.mediawiki.ltr.sitedir-ltr.mw-hide-empty-elt.ns--1.ns-special.mw-special-Prefixindex.page-Special_PrefixIndex.rootpage-Special_PrefixIndex.skin-vector.action-view.skin-vector-legacy div#content.mw-body div#bodyContent.vector-body div#mw-content-text.mw-body-content div.mw-prefixindex-body ul.mw-prefixindex-list')
            wiki_list_artist.extend(wiki_list_artist_add[0].get_text()[1:-1].split(sep='\n '))
            last = wiki_list_artist[-1]
        except:
            print('End of wikipedia artist_list')
            break
    return pd.DataFrame({'artists': wiki_list_artist})

# Function to load data from billboard.csv or update csv by scraping from url
def load_or_scrape(source):
    '''
    Input
    ---------
    source: billboard100 - Top 100 Hits on https://www.billboard.com/charts/hot-100/
            wiki_artist - List of artist with list of songs on wikipedia.org 
    '''

    df = pd.DataFrame()
    source_dic = {
        'billboard100':{
            'filepath'  : 'data/billboard_top100.csv',
            'url'       : 'https://www.billboard.com/charts/hot-100/',
            'scraper'   : scrape_top100
            },
        'wiki_artist':{
            'filepath'  : 'data/wikipedia_artist_list.csv',
            'url' : 'https://en.wikipedia.org/wiki/Special:PrefixIndex?prefix=List+of+songs+recorded+by&namespace=0&stripprefix=1',
            'scraper'   : scrape_wiki_artist
        }
    }

    if source in source_dic.keys():
        filepath = source_dic[source]['filepath']
        url = source_dic[source]['url']
        scraper = source_dic[source]['scraper']

        try:
            import os, time
            filedate = os.stat(filepath)
            age = (time.time()-filedate.st_mtime)/60/60 
            if age >= 6:
                sh = scrape_html(url)
                try:
                    df = scraper(sh[0])
                    df.to_csv(filepath,index=False)
                except:
                    df = pd.read_csv(filepath)
                    print('Was not able to scrape data from',url,'. Statuscode:',sh[2])
            else:
                df = pd.read_csv(filepath)
        except:
            sh = scrape_html(url)
            try:
                df = scraper(sh[0])
                df.to_csv(filepath,index=False)
            except:
                print('Was not able to scrape data from',url,'. Statuscode:',sh[2])
    else:
        print('source has no scrape-entry. Please try other source')
    return df

# Define function to recommend song
def recommend_song():
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

