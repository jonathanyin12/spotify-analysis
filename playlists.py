
from tqdm import tqdm
from tracks import get_tracks_data, track_meta_cols, track_feature_cols
from utils import convert_to_df, ComplexRadar
import pandas as pd
from config import sp
import matplotlib.pyplot as plt
import numpy as np

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


def compare_playlists(playlist_stats):
    fig = plt.figure(figsize=(12, 12))
    mins = np.array(pd.DataFrame.min(playlist_stats.iloc[:, 1:], axis=0))
    maxes = np.array(pd.DataFrame.max(playlist_stats.iloc[:, 1:], axis=0))

    for i in range(len(mins)):
        if mins[i] < 0:
            mins[i] *= 1.2
        else:
            mins[i] *= 0.833

        if maxes[i] < 0:
            maxes[i] *= 0.833
        else:
            maxes[i] *=1.2

    ranges = tuple(zip(mins, maxes)) 

    radar = ComplexRadar(fig, tuple(track_feature_cols), ranges)
    playlists = []
    for playlist in np.array(playlist_stats):
        playlist_ = radar.plot(playlist[1:], label = playlist[0])
        radar.fill(playlist[1:], alpha=0.1)
        playlists.append(playlist_[0])

    radar.ax.legend(handles=playlists)
    plt.show()