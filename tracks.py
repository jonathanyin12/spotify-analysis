
from tqdm import tqdm
from config import sp


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
    return [features[feature] for feature in track_feature_cols]

def get_track_data(meta, features):
    track_meta = get_track_meta(meta)
    track_features = get_track_features(features)
    track_data = track_meta + track_features
    return track_data


def get_tracks_data(ids):
    tracks_data = []
    for chunk in tqdm(range(0, len(ids), 50)):
        chunk_meta = sp.tracks(ids[chunk: chunk+50])['tracks']
        chunk_features = sp.audio_features(ids[chunk:chunk+50])
        for i in range(len(chunk_meta)):
            track_data = get_track_data(chunk_meta[i], chunk_features[i])
            tracks_data.append(track_data)

    return tracks_data


