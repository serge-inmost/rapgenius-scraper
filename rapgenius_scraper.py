# -*- coding: utf-8 -*-
"""Rapgenius Webscraper

The script uses the rapgenius landing page of each artist to gather links to
individual songs, then browse each song page to gather lyrics and new song
links.

Directions:
    Provide list of artists in file artists.txt, separated by line break (\n).
    Each artist name must match his name on the website.
    Examples:
         Pete Rock & C.L. Smooth as "Pete-rock-and-cl-smooth"
         Mos Def as "Yasiin-bey"
        
    Provide your uner agent in user_agent, you can find it on
    https://www.whatismybrowser.com/detect/what-is-my-user-agent
    
    Provide proxy information (if needed) in proxies
    
    Output produced in output.txt
"""

from bs4 import BeautifulSoup
import requests
import io

# Allows python 2/3 compatibility
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

def check_presence(mystring, mylist):
    """Check if any string element of mylist in encountered in mystring, 
    returns boolean.
    """
    if any(ext in mystring for ext in mylist):
        return True
    else:
        return False
    
def get_lyrics(mydic):
    """For each url key in source dictionary, connects to url, stores lyrics
    (if exists) as value, gather new relevant links to feed dictionary. Returns
    dictionary with lyrics provided for original keys, plus additional keys.
    """
    print('Original keys nb: ' + str(len(mydic.keys())))
    new_keys = []
    for url in mydic.keys():
        if mydic[url] == 'no lyrics':
            print('Connecting to ' +url)
            response = requests.get(url, 
                                    headers={'User-Agent': user_agent},
                                    proxies=proxies)
            soup = BeautifulSoup(response.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                if ('-lyrics' in a['href'] 
                        and '#note-' not in a['href'] 
                        and '/posts/' not in a['href'] 
                        and check_presence(a['href'],
                                           [artist+'-' for artist in artists]) 
                        and a['href'] not in mydic.keys() 
                        and a['href'] not in new_keys ) :
                    print('Adding to dic: ' + a['href'])
                    new_keys.append(a['href'])
            if mydic[url] == 'no lyrics':
                print('Updating lyrics for: ' + url)
                try:
                    mydic[url] = soup.find('div', class_='lyrics').text.strip()
                except:
                    mydic[url] = ''
    for key in new_keys:
        mydic.update({key : 'no lyrics'})
    print('Final keys nb: ' + str(len(mydic.keys())))
    return mydic

proxies = {
  'http': 'http://user:password@host/',
  'https': 'http://user:password@host/',
}

user_agent = ('Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36')

with open('artists.txt', 'r') as myfile:
    artists = [line for line in myfile.readlines()]
artists = [x.strip('\n') for x in artists]

lyrics = {}

# Connect to each artist's landing page, grab the links to featured songs and
# store them in the dictionary
for artist in artists:
    artist_url = "http://genius.com/artists/" + artist
    print('Connecting to ' + artist_url)
    response = requests.get(artist_url, headers={'User-Agent': user_agent},
                            proxies=proxies)
    soup = BeautifulSoup(response.text, 'html.parser')
    for a in soup.find_all('a', href=True):
        if ('-lyrics' in a['href'] 
                and '#note-' not in a['href'] 
                and '/posts/' not in a['href']
                and check_presence(a['href'],
                                   [artist+'-' for artist in artists])
                and a['href'] not in lyrics.keys()) :
            print('Adding to dic: ' + a['href'])
            lyrics.update({a['href'] : 'no lyrics'})

n_keys = [len(lyrics.keys())]

# Run the function at least once (get lyrics and search for more links)
lyrics = get_lyrics(lyrics)

n_keys.append(len(lyrics.keys()))

# Run the function until no more new links are found
while n_keys[len(n_keys)-1] != n_keys[len(n_keys)-2]:
    lyrics = get_lyrics(lyrics)
    n_keys.append(len(lyrics.keys()))

# Write the final lyrics down to a text file
# My use case was creating a complete lyrics corpus for NLP, so I didn't
# bother with song/artist information and separation. Could be tweaked.    
with io.open("output.txt", "a", encoding="utf-8") as myfile:
    for key,value in lyrics.items():
        myfile.write(value)
        myfile.write('\n\n')


