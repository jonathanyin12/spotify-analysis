
from tqdm import tqdm
from utils import sp, convert_to_df


track_meta_cols =  ['name', 'album', 'artist', 'spotify_url', 'popularity', 'duration', 'explicit']
track_feature_cols = ['acousticness', 'danceability', 'energy', 
                    'instrumentalness', 'loudness',
                     'tempo', 'valence']

def get_track_meta(meta):
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    spotify_url = meta['external_urls']['spotify']
    # album_cover = meta['album']['images'][0]['url']
    popularity = meta['popularity']
    duration = meta['duration_ms']
    explicit = meta['explicit']    
    track_meta = [name, album, artist, spotify_url, popularity, duration, explicit]
    return track_meta

def get_track_features(features):
    try:
        features = [features[feature] for feature in track_feature_cols]
    except:
        features = None
    return features

def get_track_data(meta, features):
    track_meta = get_track_meta(meta)
    track_features = get_track_features(features)
    if track_features:
        track_data = track_meta + track_features
        return track_data
    else:
        return None
    

def get_tracks_data(ids):
    tracks_data = []
    for chunk in tqdm(range(0, len(ids), 50)):
        chunk_meta = sp.tracks(ids[chunk: chunk+50])['tracks']
        chunk_features = sp.audio_features(ids[chunk:chunk+50])
        for i in range(len(chunk_meta)):
            track_data = get_track_data(chunk_meta[i], chunk_features[i])
            if track_data:
                tracks_data.append(track_data)
    return tracks_data

def get_liked_tracks():
    tracks_ids = get_liked_tracks_ids()
    tracks_data = get_tracks_data(tracks_ids)
    df = convert_to_df(tracks_data, columns= track_meta_cols+track_feature_cols)
    return df


def get_liked_tracks_ids():
    liked_tracks = []
    offset = 0
    while True:
        tracks = sp.current_user_saved_tracks(offset=offset, limit=50)['items']
        if len(tracks) == 0:
            break
        else:
            liked_tracks.extend(tracks)
            offset+=50

    track_ids = []
    for song in tqdm(liked_tracks):
        if song['track']['id']:
            track_ids.append(song['track']['id'])
    return track_ids


def get_top_tracks_ids(time_frame='long_term', limit=50):
    top_tracks = sp.current_user_top_tracks(limit=limit, offset=0, time_range=time_frame)
    track_ids = []
    for track in tqdm(top_tracks['items']):
        if track['id']:
            track_ids.append(track['id'])
    return track_ids


def get_top_tracks(time_frame='long_term', limit=50):
    tracks_ids = get_top_tracks_ids(time_frame, limit)
    tracks_data = get_tracks_data(tracks_ids)
    df = convert_to_df(tracks_data, columns= track_meta_cols+track_feature_cols)
    return df