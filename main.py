import requests


def last_fm_requests(payload):
    headers = {
        'user-agent': USER_AGENT
    }
    url='https://ws.audioscrobbler.com/2.0/'
    r = requests.get(url, headers = headers, params = payload)
    return r.status_code

API_KEY = 'c388e2286deda45d940563f3fae64a21'
USER_AGENT = 'MusicAPI'
payload = {
    'api_key': API_KEY,
    'method': 'chart.gettopartists',
    'format': 'json'
}
print(last_fm_requests(payload))