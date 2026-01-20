import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import json

# Read Spotify credentials from a config file
config_file = open("./config.txt", "r")
string = config_file.read()
settings = json.loads(string)

SPOTIPY_CLIENT_ID = settings['client_id']
SPOTIPY_CLIENT_SECRET = settings['client_secret']
SPOTIPY_REDIRECT_URI = 'http://localhost:5000/callback'
SCOPE = 'playlist-read-private'

# Initialize Spotify client with OAuth authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE
))

# Get playlists of the current user
playlists = sp.current_user_playlists()

playlist_data = {}

# For each playlist retrieved
for playlist in playlists['items']:
    # Get the playlist ID
    playlist_id = playlist['id']
    # Get the playlist name
    playlist_name = playlist['name']
    # Get the tracks in the playlist
    tracks = sp.playlist_tracks(playlist_id)
    # List to store the songs in the playlist
    playlist_tracks = []
    # For each track in the playlist
    for track in tracks['items']:
        # Get the track name
        track_name = track['track']['name']
        # Add the track name to the playlist_tracks list
        playlist_tracks.append(track_name)
    # Add the playlist and its tracks to the playlist_data dictionary
    playlist_data.update({playlist_name: playlist_tracks})
