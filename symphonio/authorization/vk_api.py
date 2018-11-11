import requests

API_VERSION = '5.87'
OAUTH_AUTHORIZE_URL = 'https://oauth.vk.com/authorize/'
OAUTH_ACCESS_TOKEN_URL = 'https://oauth.vk.com/access_token/'
API_URL = 'https://api.vk.com/method/'
REDIRECT_URI = 'http://localhost:8000/auth/receive_token/'
EMAIL_SCOPE = 4194304
CLIENT_ID = '6747392'
SECRET_KEY = 'qzEcAtyYg5eTzbdfm6mb'


def get_authorization_url():
    data = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'display': 'page',
        'scope': str(EMAIL_SCOPE),
        'response_type': 'code',
        'v': API_VERSION,
    }
    url = OAUTH_AUTHORIZE_URL[:-1] + "?"
    for k, v in data.items():
        url += "&%s=%s" % (k, v)
    return url


def get_auth_info(code):
    data = {
        'client_id': CLIENT_ID,
        'client_secret': SECRET_KEY,
        'redirect_uri': REDIRECT_URI,
        'code': code,
    }
    r = requests.post(OAUTH_ACCESS_TOKEN_URL, data=data)
    return r.json()


def get_bdate_and_sex(token, vk_id):
    METHOD = 'users.get'
    r = requests.post(
        API_URL + METHOD, data={
            'user_ids': vk_id,
            'fields': 'bdate,sex,first_name,last_name',
            'access_token': token,
            'v': API_VERSION,
        })
    json = r.json()
    user_row = json['response'][0]
    return user_row.get('bdate'), \
           user_row.get('sex'), \
           user_row.get('first_name'), \
           user_row.get('last_name')
