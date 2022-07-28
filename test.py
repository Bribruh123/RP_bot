import requests
import json
from datetime import datetime
import base64
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import threading



headers = {
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://radioparadise.com/',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
}

response = requests.get('https://api.radioparadise.com/api/auth', headers=headers)

print(response.text)

auth_json = response.json()



cookies = {
    'player_id': 'rp3_5480145e-e00a-1505-c5f3-80d90362ce20',
    'C_user_id': auth_json['user_id'],
    'country_code': 'US',
    'C_username': 'anonymous',
    'source': '24',
}


headers = {
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://radioparadise.com/',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
    }



indx = 0
songs = []
while(indx<4):
    params = {
        'file': 'music::play-history',
        'channel': '0',
        'list_offset': indx*20
    }

    response = requests.get('https://api.radioparadise.com/siteapi.php', params=params, cookies=cookies, headers=headers)

    songs_json = response.json()
    songs.extend(songs_json['songs'])
    print(len(songs))
    indx=indx+1
    pass

print(songs)
cnt = 0
for song in songs:
    if song['title'] == "Gravity Rides Everything":
        print("found")
        print(cnt)
    cnt = cnt+1