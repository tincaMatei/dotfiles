import requests
import json
import time
import sys
import os

environ = os.environ

cutoffs = (1200, 1400, 1600, 1900, 2100, 2300, 2400, 2600, 3000)
colors = ("#cccccc", "#77ff77", "#77ddbb", "#aaaaff", "#ff88ff", "#ffcc88", "#ffbb55", "#ff7777", "#ff3333", "#aa0000")

def return_nothing():
    res = {
        "rating": "????",
        "color": "rgba(0, 0, 0, 0.5)"
    }
    print(json.dumps(res))
    exit(0)

handle = environ["EWW_CODEFORCES_HANDLE"]

try:
    req = requests.get('https://codeforces.com/api/user.rating?handle=' + handle).json()

    if req['status'] != "OK":
        return_nothing()
    if req['result'] is None:
        return_nothing()

    changes = req['result']
    if len(changes) == 0:
        return_nothing()
    
    last = changes[-1];
    if last['newRating'] is None:
        return_nothing()

    rating = last['newRating']
    i = 0
    while i < len(cutoffs) and rating >= cutoffs[i]:
        i = i + 1

    res = {
        "rating": str(rating),
        "color": colors[i]
    }
    print(json.dumps(res))
    sys.exit(0)
except (SystemExit):
    pass
except:
    return_nothing()
