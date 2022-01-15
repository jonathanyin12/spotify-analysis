
from tqdm import tqdm
from tracks import get_tracks_data, track_meta_cols, track_feature_cols
from utils import sp, convert_to_df
import pandas as pd

user_playlists = sp.current_user_playlists()['items']
user_playlist_ids = {playlist['name']: playlist['id'] for playlist in user_playlists}


def get_playlist_tracks_ids(playlist_id):
    playlist_tracks = []
    offset = 0
    while True:
        tracks = sp.playlist_items(playlist_id, limit=50, offset=offset)['items']
        if len(tracks) == 0:
            break
        else:
            playlist_tracks.extend(tracks)
            offset+=50

    track_ids = []
    for track in playlist_tracks:
        if track['track'] and track['track']['id']:
            track_ids.append(track['track']['id'])
    return track_ids


def get_playlist_data(playlist):
    playlist_id = user_playlist_ids[playlist]
    track_ids = get_playlist_tracks_ids(playlist_id)
    data = get_tracks_data(track_ids)
    return convert_to_df(data, columns= track_meta_cols+track_feature_cols)


def get_playlist_stats(playlist):
    df = get_playlist_data(playlist)
    features = df.loc[:, 'acousticness': ]
    return list(pd.DataFrame.mean(features))

def get_playlists_stats(playlists):
    playlists_stats = []
    for name in playlists:
        data = [name]+ get_playlist_stats(name)
        playlists_stats.append(data)

    df = convert_to_df(playlists_stats, columns=['name']+track_feature_cols)
    return df