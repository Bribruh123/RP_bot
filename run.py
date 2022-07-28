import requests
import json
from datetime import datetime
import base64
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import threading



def run():
    threading.Timer(30.0, run).start()
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

    params = {
        'file': 'music::play-history',
        'channel': '0',
    }

    response = requests.get('https://api.radioparadise.com/siteapi.php', params=params, cookies=cookies, headers=headers)

    songs_json = response.json()




    client_id = 'ff3a8d66f4a2415ba13116f4c00a18e6'
    client_secret = '29b781ee0a574eca98e2aa1630fb4342'

    auth_code = requests.get('https://accounts.spotify.com/authorize', {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': 'https://open.spotify.com/collection/playlists',
        'scope': 'playlist-modify-private',
    })
    print(auth_code.text)
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.urlsafe_b64encode((client_id + ':' + client_secret).encode())
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic %s' % auth_header.decode('ascii')
    }
    data = {
        'grant_type': 'client_credentials',
        # 'client_id': client_id,
        # 'client_secret': client_secret,
        'code' : auth_code,
        'scope': 'playlist-modify-private'
    }
    auth_response = requests.post(auth_url, data=data, headers=headers)
    access_token = auth_response.json().get('access_token')

    title = songs_json['songs'][0]['title']
    print(title)
    artist = songs_json['songs'][0]['artist']
    print(artist)
    playtime = songs_json['songs'][0]['play_time']
    print(playtime)

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token),
    }

    params = {
        'q': 'artist:{} track:{}'.format(artist, title),
        'type': 'track',
        'market': 'US',
        'limit': '50',
        'offset': '0',
    }

    response = requests.get('https://api.spotify.com/v1/search', params=params, headers=headers)

    songs = []

    print(response)

    for item in response.json()['tracks']['items']:
        print('name ', item['name'])
        print('artist ', item['artists'][0]['name'])
        print('id ', item['id'])
        if item['artists'][0]['name'] == artist:
            print('name ', item['name'])
            print('artist ', item['artists'][0]['name'])
            print('id ', item['id'])
            print('\n')
            songs.append({'name ': item['name'], 'artist ': item['artists'][0]['name'], 'id': item['id'], 'playtime': playtime})

    for item in songs:
        print(item)


    if not songs:
        with open('list_not_found.txt') as f:
            if title not in f.read():
                f_add = open("list_not_found.txt", "a")
                f_add.write(json.dumps({'name ': title, 'artist ': artist, 'playtime': playtime}))
                f_add.close()
        f.close()

    else:

        with open('list_found.txt') as f:
            if songs[0]['id'] not in f.read():
                f_add = open("list_found.txt", "a")
                f_add.write(json.dumps(songs[0]) + '\n')
                f_add.close()
                username='1227122799'
                os.environ["SPOTIPY_CLIENT_ID"] = "ff3a8d66f4a2415ba13116f4c00a18e6"
                os.environ["SPOTIPY_CLIENT_SECRET"] = "29b781ee0a574eca98e2aa1630fb4342"
                os.environ["SPOTIPY_REDIRECT_URI"] = "http://example.com"
                scope = 'playlist-modify-public'


                sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
                sp.playlist_add_items('12PfopLD2DGo1UWTtQ69RX', [songs[0]['id']])

        f.close()


run()

