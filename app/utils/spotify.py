from os import getenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyClient:
    def __init__(self):
        self.client=Spotify(
            auth_manager = SpotifyClientCredentials(
                client_id = getenv('SPOTIFY_CLIENT_ID'),
                client_secret = getenv('SPOTIFY_CLIENT_SECRET'),
            )
        )

    def searchTrack(self, search):
        return  self.client.search(
                q=search,
                type='track'
            )