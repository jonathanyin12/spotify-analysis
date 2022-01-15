
from tqdm import tqdm
from tracks import get_tracks_data
from utils import sp, convert_to_df

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


def get_playlist_data(playlist_id):
    track_ids = get_playlist_tracks_ids(playlist_id)
    data = get_tracks_data(track_ids)
    return convert_to_df(data)