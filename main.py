import requests
import requests_cache
import json
import time
import pandas as pd
from tqdm import tqdm
from IPython.core.display import clear_output
requests_cache.install_cache()
tqdm.pandas()

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def lookup_tags(artist):
    response = last_fm_requests({
        'api_key': API_KEY,
        'method': 'artist.getTopTags',
        'artist':  artist,
        'format': 'json'
    })

    # if there's an error, just return nothing
    if response.status_code != 200:
        return None

    # extract the top three tags and turn them into a string
    tags = [t['name'] for t in response.json()['toptags']['tag'][:3]]
    tags_str = ', '.join(tags)

    # rate limiting
    if not getattr(response, 'from_cache', False):
        time.sleep(0.25)
    return tags_str

def last_fm_requests(payload):
    headers = {
        'user-agent': USER_AGENT
    }
    url='https://ws.audioscrobbler.com/2.0/'
    r = requests.get(url, headers = headers, params = payload)
    return r

API_KEY = 'c388e2286deda45d940563f3fae64a21'
USER_AGENT = 'MusicAPI'

responses=[]
page=1
total_pages=99999

while page<=total_pages:
    payload = {
        'api_key': API_KEY,
        'method': 'chart.gettopartists',
        'limit': 500,
        'page' :page,
        'format': 'json'
    }
    print("Requesting page{}/{}".format(page,total_pages))
    clear_output(wait=True)
    response= last_fm_requests(payload)

    if response.status_code!=200:
        print(response.text)
        break
    page =int(response.json()['artists']['@attr']['page'])
    total_pages=int(response.json()['artists']['@attr']['totalPages'])
    responses.append(response)

    if not getattr(response,'from_cache', False):
        time.sleep(0.25)
    page+=1


pd.set_option('max_columns', None)
frames = [pd.DataFrame(r.json()['artists']['artist']) for r in responses]
artists = pd.concat(frames)
artists = artists.drop('image', axis=1)
#artists.info()
#print(artists.describe())
artist_counts = [len(r.json()['artists']['artist']) for r in responses]
#print(pd.Series(artist_counts).value_counts())
#print(artist_counts[:50])
artists = artists.drop_duplicates().reset_index(drop=True)
artists['tags'] = artists['name'].progress_apply(lookup_tags)
print(artists.head())