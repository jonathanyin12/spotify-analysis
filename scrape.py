from joblib import Parallel, delayed
from playlists import get_playlist_tracks_ids
from tracks import get_tracks_data, track_meta_cols, track_feature_cols
from utils import convert_to_df, sp

def get_spotify_songs():
    playlist_ids = get_spotify_playlists()
    all_tracks_ids= Parallel(n_jobs=-1,backend='threading', verbose=8)(delayed(get_playlist_tracks_ids)(id) for id in playlist_ids)
    all_tracks_ids = list(set(sum(all_tracks_ids, [])))

    # all_track_ids = set()
    # for id in tqdm(playlist_ids):
    #     track_ids = get_playlist_tracks_ids(id)
    #     all_track_ids.update(track_ids)

    tracks_data = get_tracks_data(all_tracks_ids)
    df = convert_to_df(tracks_data, columns= track_meta_cols+track_feature_cols)
    return df

def get_spotify_playlists():
    playlists = []
    offset = 0
    while True:
        chunk =sp.user_playlists('spotify', offset=offset)['items']
        if len(chunk) == 0:
            break
        else:
            playlists.extend(chunk)
            offset+=50
    playlist_ids = [playlist['id'] for playlist in playlists]
    return playlist_ids

