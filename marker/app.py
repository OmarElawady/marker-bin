
from flask import *
import json
from flask_oauth import OAuth
from urllib.request import *
from urllib.error import *
from flask_github import GitHub
from github import Github as git
from peewee import *
import pygments
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

database = SqliteDatabase('app.db')

class BaseMode(Model):
    class Meta:
        database = database

class User(BaseMode):
    username = CharField( unique = True)
    password = CharField()
    email = CharField()

class Src(BaseMode):
    text = TextField()
    language  = CharField()
    user = ForeignKeyField(User, backref='srcs')

def create_tables():
    database.create_tables([User, Src])

def mark(text):
    #styles >> HtmlFormatter().get_style_defs('.highlight')
    return pygments.highlight(text, PythonLexer(), HtmlFormatter())


# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
GOOGLE_CLIENT_ID = '42073104430-pmelurs143kkkm5mbh1cqd58o7kptgsg.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'Uu1CaNcwKAOxyFgbTh-qR1jM'
GOOGLE_REDIRECT_URI = '/googleoauth2callback'  # one of the Redirect URIs from Google APIs console
GIT_CLIENT_ID='1d3f2d20958f5563461d'
GIT_CLIENT_SECRET='2dbcb4911df26167ade0323bfe29f4eadecb2a73'
GIT_REDIRECT_URI='/gitoauth2callback'

SECRET_KEY = 'development key'
DEBUG = True

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()
app.config['GITHUB_CLIENT_ID'] = GIT_CLIENT_ID
app.config['GITHUB_CLIENT_SECRET'] = GIT_CLIENT_SECRET

# For GitHub Enterprise
app.config['GITHUB_BASE_URL'] = 'https://api.github.com/'
app.config['GITHUB_AUTH_URL'] = 'https://github.com/login/oauth/'

github = GitHub(app)

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

def getUser():
    user = session.get('user')
    if user is not None:
        user=json.loads(user.replace('\'','\"'))
        return user
    return None

def getUserName():
    user=getUser();
    if user is not None:
        return user['name']
    return None

def getUserEmail():
    user=getUser();
    if user is not None:
        return user['email']
    return None

def getUserPicture():
    user=getUser();
    if user is not None:
        return user['picture']
    return None

@app.route('/logout')
def logout():
    session.pop('user',None)
    return "logged out"

@app.route('/')
def index():
    user=getUser()
    if user is not None:
        return getUserName()+ getUserEmail()+getUserPicture()
    return "None"

@app.route('/loginGit')
def loginGit():
    return github.authorize()

@app.route(GIT_REDIRECT_URI)
@github.authorized_handler
def authorizedGit(oauth_token):
    if oauth_token is None:
        flash("Authorization failed.")
        return redirect(url_for('index'))
    g=git(oauth_token)
    user=g.get_user()
    userData={"email":user.get_emails()[0]['email'],"name":user.login,"picture":user.avatar_url}
    session['user']=str(userData)
    print( session['user'])
    return userData


@app.route('/loginGoogle')
def loginGoogle():
    callback=url_for('authorizedGoogle', _external=True)
    return google.authorize(callback=callback)

@app.route(GOOGLE_REDIRECT_URI)
@google.authorized_handler
def authorizedGoogle(resp):
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



if __name__ == '__main__':
    app.run()
