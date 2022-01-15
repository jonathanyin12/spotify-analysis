from utils import convert_to_df
from config import sp

def get_artist_data(artist_id):
    artist = sp.artist(artist_id)
    fields = ['name', 'genres', 'popularity']
    artist_meta = [artist[field] for field in fields] + [artist['followers']['total']]
    return artist_meta


def get_top_artists(time_range = 'long_term', limit=50):
    top_artist = sp.current_user_top_artists(limit=limit, offset=0, time_range=time_range)['items']
    artists_data = [get_artist_data(artist['id']) for artist in top_artist]
    artist_df = convert_to_df(artists_data, columns=['name', 'genre', 'popularity', 'followers'])
    return artist_df
