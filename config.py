import os

basedir = os.path.abspath(os.path.dirname(__name__))

class Config:
    SECRET_KEY = "Something about words..."
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:NKd#!a$Ff58X@localhost:5432/indie_music'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SQLALCHEMY_DATABASE_URI = os.environ.get('')
    # for when we use the heroku