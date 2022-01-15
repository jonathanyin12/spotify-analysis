import pandas as pd 
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SCOPE
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, 
                                               client_secret=SPOTIPY_CLIENT_SECRET, 
                                               redirect_uri=SPOTIPY_REDIRECT_URI, 
                                               scope=SCOPE))


def convert_to_df(tracks_data, columns):
    df = pd.DataFrame(tracks_data, columns =columns)
    return df



    