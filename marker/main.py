#pip install git+https://github.com/mitsuhiko/flask-oauth

from flask import *
import json
from flask_oauth import OAuth
from urllib.request import *
from urllib.error import *
# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
GOOGLE_CLIENT_ID = '42073104430-pmelurs143kkkm5mbh1cqd58o7kptgsg.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'Uu1CaNcwKAOxyFgbTh-qR1jM'
GOOGLE_REDIRECT_URI = '/oauth2callback'  # one of the Redirect URIs from Google APIs console


SECRET_KEY = 'development key'
DEBUG = True

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

google = oauth.remote_app('google',
base_url='https://www.google.com/accounts/',
authorize_url='https://accounts.google.com/o/oauth2/auth',
request_token_url=None,
request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
'response_type': 'code'},
access_token_url='https://accounts.google.com/o/oauth2/token',
access_token_method='POST',
access_token_params={'grant_type': 'authorization_code'},
consumer_key=GOOGLE_CLIENT_ID,
consumer_secret=GOOGLE_CLIENT_SECRET)

@app.route('/')
def index():
    user = session.get('user')
    if user is None:
        return redirect(url_for('loginGoogle'))
    else:
        user=json.loads(user)
        return user['email']



@app.route('/loginGoogle')
def loginGoogle():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)

@app.route(GOOGLE_REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    access_token=access_token,''
    access_token = access_token[0]
    headers = {'Authorization': 'OAuth ' + access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',None, headers)
    try:
        res = urlopen(req)
    except URLError as e:
        return str(e)
    userData=''
    for lines in res.readlines():
        userData+=str(lines)
    data = userData.replace('b\'', '')
    data = data.replace('\\n','')
    data = data.replace('\'', '')
    print(data)
    session['user']=data
    return data


@google.tokengetter
def get_access_token():
    return session.get('access_token')

if __name__ == '__main__':
    app.run()