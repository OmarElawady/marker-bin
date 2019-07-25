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
    owner = ForeignKeyField(User, db_column='owner', related_name='srcs', to_field='email')

def create_tables():
    database.create_tables([User, Src])



def mark_text(src_text, src_language):
    """return the marked text"""
    #styles >> HtmlFormatter().get_style_defs('.highlight')
    lexer = get_lexer_by_name(src_language, stripall=True)
    text = pygments.highlight(src_text, lexer , HtmlFormatter())
    return text



def add_user(user_username, user_password, user_email):
    """save new user to the database"""
    user = User(username=user_username, password= user_password, email=user_email)
    user.save()




def add_src(src_text, src_language, src_owner_email):
    """save source code text in the database"""
    src = Src(text=src_text, language=src_language, owner=src_owner_email)
    src.save()
    return src.id


def get_srcs_by_email(user_email):
    """return list for all the quaries the email has"""
    quaries = Src.select().join(User).where(User.email == user_email)
    return list(quaries)



def get_src_by_id(src_id):
    """return a tuple have the text and the language of the code"""
    try:
        quary = Src.select().where(Src.id == src_id).get()
        return quary.text, quary.language
    except Src.DoesNotExist:
        return None


def check_for_user_by_username(user_username): ##
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



def login_by_username(user_username, user_password): ##
    """give the access for the user to Email"""
    try:
        quary = User.select().where(User.username == user_username , User.password==user_password).get()
        return True
    except User.DoesNotExist:
        return False



def login_by_email(user_email, user_password):
    """give the access for the user to Email"""
    try:
        quary = User.select().where(User.email == user_email , User.password==user_password).get()
        return quary.username
    except User.DoesNotExist:
        return None