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


