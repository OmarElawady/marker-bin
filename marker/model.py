from peewee import *
import pygments
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

database = SqliteDatabase('model.db')

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
    owner = ForeignKeyField(User, db_column='owner', related_name='srcs', to_field='username')

def create_tables():
    database.create_tables([User, Src])

def mark(text):
    #styles >> HtmlFormatter().get_style_defs('.highlight')
    return pygments.highlight(text, PythonLexer(), HtmlFormatter())

def get_srcs_by_username(user_username):
    quary = Src.select().join(User).where(User.username == user_username).get()
    return quary.text

def get_src_by_id(src_id):
    quary = Src.select().where(Src.id == src_id).get()
    return quary.text

def add_user(user_username, user_password, user_email):
    user = User(username=user_username, password= user_password, email=user_email)
    user.save()
    return f'{user_username} is created'

def check_for_user(user_username):
    query = User.select().where(User.username == user_username)
    if query.exists():
        return f'{user_username} exists, try to login'

def add_src(src_text, src_language, src_owner):
    src = Src(text=src_text, language=src_language, owner=src_owner)
    src.save()
    return 'code is created'

