from flask import Blueprint, request, jsonify
from indie_music_inv.helpers import token_required
from indie_music_inv.models import Song, db, song_schema, songs_schema
api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'Test_data': 1000, 'Tests': 'me'}

@api.route('/songs', methods=['POST'])
@token_required
def create_song(current_user_token):
    artists = request.json['artists']
    album = request.json['album']
    songs = request.json['songs']
    release_date = request.json['release_date']
    explicit = request.json['explicit']
    cost = request.json['cost']
    download_link = request.json['download_link']
    artist_page = request.json['artist_page']
    token = current_user_token.token

    print(f'TEST: {current_user_token.token}')

    song = Song(artists, album, songs, release_date, explicit, cost, download_link, artist_page, user_token = token)
    
    db.session.add(song)
    db.session.commit()
    response = song_schema.dump(song)
    return jsonify(response)

@api.route('/songs', methods= ['GET'])
@token_required
def get_songs(current_user_token):
    owner = current_user_token.token
    songs = Song.query.filter_by(user_token = owner).all()
    response = songs_schema.dump(songs)
    return jsonify(response)

@api.route('/songs/<id>', methods= ['GET'])
@token_required
def get_song(current_user_token, id):
    song = Song.query.get(id)
    print(f'Here is your Listing for: {song.artists}')
    response = song_schema.dump(song)
    return jsonify(response)

@api.route('/songs/<id>', methods = ['POST', 'PUT'])
@token_required
def update_song(current_user_token, id):
    song = Song.query.get(id)
    print(song)
    if song:
        song.artists = request.json['artists']
        song.album = request.json['album']
        song.songs = request.json['songs']
        song.release_date = request.json['release_date']
        song.explicit = request.json['explicit']
        song.cost = request.json['cost']
        song.download_link = request.json['download_link']
        song.artist_page = request.json['artist_page']
        song.token = current_user_token.token

        db.session.commit()
        response = song_schema.dump(song)
        return jsonify(response)
    else:
        return jsonify({'Error:' 'That song does not exist!'})

@api.route('/songs/<id>', methods = ['DELETE'])
@token_required
def delete_song(current_user_token, id):
    song = Song.query.get(id)
    print(song)
    if song:
        db.session.delete(song)
        db.session.commit()

        return jsonify({'Success': f'Song ID: {song.id} has been deleted'})
    else:
        return jsonify({'Error': 'That song does not exist!'})