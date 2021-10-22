from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    
    def __init__(self, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)
    
    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        return generate_password_hash(password)
        
    
    def set_token(self, length):
        return secrets.token_hex(length)

class Song(db.Model):
    id = db.Column(db.String, primary_key=True)
    artists = db.Column(db.String(300))
    album = db.Column(db.String(150), nullable = True)
    songs = db.Column(db.String(300))
    release_date = db.Column(db.String(20))
    explicit = db.Column(db.String(10))
    cost = db.Column(db.Numeric(precision=5, scale=2), nullable = True)
    download_link = db.Column(db.String(300), nullable = True)
    artist_page = db.Column(db.String(300), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, artists, album, songs, release_date, explicit, cost, download_link, artist_page, user_token, id = ''):
        self.id = self.set_id()
        self.artists = artists
        self.album = album
        self.songs = songs
        self.release_date = release_date
        self.explicit = explicit
        self.cost = cost
        self.download_link = download_link
        self.artist_page = artist_page
        self.user_token = user_token

    def set_id(self):
        return(secrets.token_urlsafe())

class SongSchema(ma.Schema):
    class Meta:
        fields = ['id', 'artists', 'album', 'songs', 'release_date', 'explicit', 'cost', 'download_link', 'artist_page']
    
song_schema = SongSchema()
songs_schema = SongSchema(many=True)