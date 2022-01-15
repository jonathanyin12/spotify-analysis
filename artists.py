from utils import convert_to_df
from config import sp
from collections import Counter

def get_artist_data(artist_id):
    artist = sp.artist(artist_id)
    fields = ['name', 'genres', 'popularity']
    artist_meta = [artist[field] for field in fields] + [artist['followers']['total']]
    return artist_meta


def get_top_artists(time_range = 'long_term', limit=50):
    top_artists = sp.current_user_top_artists(limit=limit, offset=0, time_range=time_range)['items']
    artists_data = []
    fields = ['name', 'genres', 'popularity']
    for artist in top_artists:
        artist_meta = [artist[field] for field in fields] + [artist['followers']['total']]
        artists_data.append(artist_meta)
    artist_df = convert_to_df(artists_data, columns=['name', 'genre', 'popularity', 'followers'])
    return artist_df


def get_top_genres(time_range = 'long_term', limit=10):
    genres = []
    top_artist = sp.current_user_top_artists(limit=50, offset=0, time_range=time_range)['items']
    for artist in top_artist:
        genres.extend(artist['genres'])
    genres = Counter(genres)
    return genres.most_common(n = limit)