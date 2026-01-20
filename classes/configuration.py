import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class Configuration:

    def __init__(self):
        config_file = open("./config.txt", "r")
        string = config_file.read()
        settings = json.loads(string)
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=settings['client_id'],
                                                            client_secret=settings['client_secret'])) 
        if 'view' in settings:
            if  settings['view'] == "True":
                self.view = True
            elif settings['view'] == "False":
                self.view = False
        else:
            self.view = False


    def getSpotify(self):
        return self.sp
    
    def getView(self):
        return self.view