# Standard Modules
import requests


# Third-party Modules
from bs4 import BeautifulSoup
from telebot.types import Message


# Variables
animesearch_url = "https://myanimelist.net/search/all?q={}&cat=all"
animetop_url = "https://myanimelist.net/topanime.php?limit={}"
youtube_url = "https://www.youtube.com/watch?v={}"


def search(title: str) -> list:
    
    title_split = [word.lower() for word in title.split(" ")]
    title = "%20".join(title_split)
    
    search_results = []
    
    website = requests.get(animesearch_url.format(title))
    soup = BeautifulSoup(website.text, "lxml")
    
    a_tags = soup.find_all("a", class_="hoverinfo_trigger fw-b fl-l")
    
    match = 0
    
    for a_tag in a_tags:
        match = 0
        for word in title_split:
            if word in a_tag.text.lower():
                match += 1
        if match >= len(title_split):
            search_results.append([a_tag.text, a_tag['href']])
    
    return search_results


def ranking() -> list:
    
    rankings = []
    
    for round in range(2):
        
        if round == 1:
            limit = 50
        else:
            limit = 0
            
        website = requests.get(animetop_url.format(limit))
        soup = BeautifulSoup(website.text, "lxml")
        
        h3_tags = soup.find_all("h3", class_="anime_ranking_h3")
        
        for h3_tag in h3_tags:
            a_tag = h3_tag.find("a")
            rankings.append(a_tag.text)
    
    return rankings


def osts(anime_url: str) -> list:
    
    website = requests.get(anime_url)
    soup = BeautifulSoup(website.text, "lxml")
    
    song_titles = soup.find_all("span", class_="theme-song-title")
    song_artists = soup.find_all("span", class_="theme-song-artist")
    
    songs = []
    
    for index in range(len(song_titles)):
        song = song_titles[index].text
        artist = song_artists[index].text
        songs.append(f"{index + 1}. {song} by {artist}\n")
        
    return songs


def find_characters(anime_url: str) -> list:
    
    website = requests.get(anime_url)
    soup = BeautifulSoup(website.text, "lxml")
    
    h3_tags = soup.find_all("h3", class_="h3_characters_voice_actors")
    
    characters = []
    
    for h3_tag in h3_tags:
        a_tag = h3_tag.find("a")
        characters.append([a_tag.text, a_tag['href']])
        
    return characters


def find_summary(anime_url: str) -> str:
    
    website = requests.get(anime_url)
    soup = BeautifulSoup(website.text, "lxml")
    
    p_tag = soup.find_all("p", itemprop="description")
        
    return p_tag[0].text


def find_trailer(anime_url: str) -> str:
    
    website = requests.get(anime_url)
    soup = BeautifulSoup(website.text, "lxml")
    
    a_tag = soup.find_all("a", class_="iframe")
    
    embed_link = a_tag[0]['href']
    stop = embed_link.find('?')
    embed_link = embed_link[:stop]
    embed_link = embed_link[::-1]
    stop = embed_link.find('/')
    embed_link = embed_link[:stop]
    link = youtube_url.format(embed_link[::-1])
    
    return link