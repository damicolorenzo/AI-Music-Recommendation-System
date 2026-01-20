import json
import spotipy  #Spotipy is a lightweight Python library for the Spotify Web API.
from spotipy.oauth2 import SpotifyClientCredentials

class Spotify_API:

    def __init__(self):
        config_file = open("config.txt", "r")
        string = config_file.read()
        dizionario = json.loads(string)
        
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=dizionario['client_id'],
                                                            client_secret=dizionario['client_secret'])) 
    
    def getSpotify(self):
        return self.sp