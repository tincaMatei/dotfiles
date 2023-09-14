import sys
import time
import requests
import json

# Get yourself a spotify token
CLIENT_ID = "XXXXXX"
CLIENT_SECRET = "XXXXXX"
REFRESH_TOKEN = "XXXXXX"
REDIRECT_URI = "http://localhost:5000/callback"

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

def send_request(method, endpoint, token):
    headers = { 'Authorization': 'Bearer ' + token }
    print("Gonna do a request at https://api.spotify.com/v1" + endpoint, file=sys.stderr)
    if method == 'post':
        resp = requests.post("https://api.spotify.com/v1" + endpoint, headers=headers)
    elif method == 'put':
        resp = requests.put("https://api.spotify.com/v1" + endpoint, headers=headers)
    
    print(json.dumps(resp.json()), file = sys.stderr)

argv = sys.argv

if len(argv) != 2:
    print("Invalid arguments", file=sys.stderr)
    exit(1)

flag = argv[1]

token = request_spotify_token()

if flag == '--next' or flag == '-n':
    send_request("post", "/me/player/next", token)
elif flag == '--prev' or flag == '-p':
    send_request("post", "/me/player/previous", token)
elif flag == '--pause' or flag == '-P':
    send_request("put", "/me/player/pause", token)
elif flag == '--play' or flag == '-s':
    send_request("put", "/me/player/play", token)
