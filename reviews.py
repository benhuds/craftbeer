# adapted from the Yelp v2 API sample code

import json
import urllib
import urllib2
import oauth2

API_HOST = 'api.yelp.com'
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = "CONSUMERKEY"
CONSUMER_SECRET = "CONSUMERSECRET"
TOKEN = "TOKEN"
TOKEN_SECRET = "TOKENSECRET"

def request(host, path, url_params=None):
    url_params = url_params or {}
    url = 'https://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    # print u'Querying {0} ...'.format(url)

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response

def search(term, location):
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'sort': 2,
    }

    return request(API_HOST, SEARCH_PATH, url_params=url_params)

def get_business(business_id):
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path)

def query_api(term, location):
    response1 = search(term, location)
    businesses = response1.get('businesses')
    return businesses[0]['rating']

    if not businesses:
        return u'No businesses for {0} in {1} found.'.format(term, location)
