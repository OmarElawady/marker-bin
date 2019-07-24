from peewee import *
import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

database = SqliteDatabase('model.db')

class BaseMode(Model):
    class Meta:
        database = database

class User(BaseMode):
    username = CharField(unique=True)
    password = CharField()
    email = CharField(unique=True)

class Src(BaseMode):
    text = TextField()
    language  = CharField()
    owner = ForeignKeyField(User, db_column='owner', related_name='srcs', to_field='username')

def create_tables():
    database.create_tables([User, Src])



def mark_text(src_text, src_language):#pass
    """return the marked text"""
    #styles >> HtmlFormatter().get_style_defs('.highlight')
    lexer = get_lexer_by_name(src_language, stripall=True)
    text = pygments.highlight(src_text, lexer , HtmlFormatter())
    return text



def get_srcs_by_username(user_username):#pass
    """return list for all the quaries the username has"""
    quaries = Src.select().join(User).where(User.username == user_username)
    return list(quaries)



def get_src_by_id(src_id):#pass
    """retuen a tuple have the text and the language of the code"""
    try:
        quary = Src.select().where(Src.id == src_id).get()
        return quary.text, quary.language
    except Src.DoesNotExist:
        return 'code not found'


def check_for_user_by_username(user_username):#pass
    """check for existing return boolen"""
    query = User.select().where(User.username == user_username)
    if query.exists():
        return True
    else :
        return False



def check_for_user_by_email(user_email):
    """check for existing return boolen"""
    query = User.select().where(User.email == user_email)
    if query.exists():
        return True
    else:
        return False



def add_user(user_username, user_password, user_email):#pass
    """save new user to the database"""
    user = User(username=user_username, password= user_password, email=user_email)
    user.save()
    return f'{user_username} is created'




def add_src(src_text, src_language, src_owner):#pass
    """save source code text in the database"""
    src = Src(text=src_text, language=src_language, owner=src_owner)
    src.save()
    return 'code is created'



def login_by_username(user_username, user_password):#pass
    """give the access for the user to Email"""
    try:
        quary = User.select().where(User.username == user_username , User.password==user_password).get()
        return True,'Welcome'
    except User.DoesNotExist:
        return False,'Incorrect username or password'



def login_by_email(user_email, user_password): #pass
    """give the access for the user to Email"""
    try:
        quary = User.select().where(User.email == user_email , User.password==user_password).get()
        return True,'Welcome'
    except User.DoesNotExist:
        return False,'Incorrect email or password'
