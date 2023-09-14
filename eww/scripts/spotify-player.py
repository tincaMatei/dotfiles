import requests
import json
import time
import sys

# You have to do some stuff to get yourself a spotify token
CLIENT_ID = "XXXXXX"
CLIENT_SECRET = "XXXXXX"
TITLE_LIMIT = 20
ARTIST_LIMIT = 35

CLIENT_TOKEN = "XXXXXX"

IMAGE_PATH = "images/album_image"

REDIRECT_URI = "http://localhost:5000/callback"
# https://accounts.spotify.com/authorize?response_type=code&client_id=XXXXXX&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fcallback&scope=user-read-playback-state%20user-modify-playback-state

REFRESH_TOKEN = "XXXXXX"

seconds_timestamp = time.time()

def sleep_synced(secs):
    global seconds_timestamp

    while time.time() - seconds_timestamp < secs:
        time.sleep(0.01)

    seconds_timestamp = time.time();

def request_spotify_token():
    while True:
        headers = { 'Content-Type': "application/x-www-form-urlencoded" }
        payload = { 
            'grant_type': 'refresh_token',
            'refresh_token': REFRESH_TOKEN,
            #'grant_type': 'authorization_code',
            #'code': CLIENT_TOKEN,
            'client_id': CLIENT_ID, 
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'scope': 'user-read-playback-state'
        }

        resp = requests.post("https://accounts.spotify.com/api/token", params=payload, headers=headers)

        respjson = resp.json()
        
        if 'access_token' in respjson:
            return respjson['access_token']
       
        sleep_synced(1)

def query_spotify_current_track(token):
    headers = { 'Authorization': 'Bearer ' + token }

    resp = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)

    return resp.json()

def download_image(url, path):
    response = requests.get(url)

    with open(path, "wb") as f:
        f.write(response.content)

last_timestamp = time.time()
token = request_spotify_token()

cached_image_url = ''

while True:
    timestamp = time.time()

    if timestamp > last_timestamp + 3600 - 10:
        last_timestamp = timestamp
        token = request_spotify_token()

    metadata = query_spotify_current_track(token)

    result = {
        'title': '',
        'artist': '',
        'image_url': '',
        'elapsed_ms': 0,
        'duration_ms': 1,
        'is_playing': False
    }

    if 'progress_ms' in metadata:
        result['elapsed_ms'] = metadata['progress_ms']

    if 'is_playing' in metadata:
        result['is_playing'] = metadata['is_playing']

    if 'item' in metadata and metadata['item'] is not None:
        metadata = metadata['item']
        
        if 'album' in metadata:
            result['image_url'] = metadata['album']['images'][0]['url']
            # print("From " + result['image_url'] + "; cached: " + cached_image_url, file=sys.stderr)
            if cached_image_url != result['image_url']:
                # print("Downloaded", file=sys.stderr)
                cached_image_url = result['image_url']
                download_image(result['image_url'], IMAGE_PATH)
            result['image_url'] = IMAGE_PATH

        if 'artists' in metadata:
            result['artist'] = ', '.join(map(lambda val: val['name'], metadata['artists']))

        if 'duration_ms' in metadata:
            result['duration_ms'] = metadata['duration_ms'];
        else:
            result['duration_ms'] = 1
            result['elapsed_ms'] = 0

        if 'name' in metadata:
            result['title'] = metadata['name'];

    if len(result['title']) > TITLE_LIMIT:
        result['title'] = result['title'][0:TITLE_LIMIT - 3]
        result['title'] = result['title'] + "..."

    if len(result['artist']) > ARTIST_LIMIT:
        result['artist'] = result['artist'][0:ARTIST_LIMIT - 3]
        result['artist'] = result['artist'] + "..."

    print(json.dumps(result))
    sys.stdout.flush()

    sleep_synced(1)

