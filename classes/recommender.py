import warnings
warnings.filterwarnings("ignore", "\nPyarrow", DeprecationWarning)
import pandas as pd
import numpy as np
from collections import defaultdict  # defaultdict is an unordered collection of data values that works like a map
from scipy.spatial.distance import cdist

class Recommender:
    number_cols = ['valence', 'year', 'acousticness', 'danceability', 'duration_ms', 'energy', 'explicit',
    'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'popularity', 'speechiness', 'tempo']

    def __init__(self, spotify):
        self.sp = spotify

    def get_track_info(self, track_id):
        """ 
        * Retrieves the name and release year of a track
        * Given a track_id, returns a dictionary {'name': name, 'year': year}
        * Input: track_id
        * Output: {'name': name, 'year': year}
        """
        track_info = self.sp.track(track_id)
        name = track_info['name']
        year = int(track_info['album']['release_date'][:4])
        track_dict = {'name': name, 'year': year}
        return track_dict

    def get_track_id(self, track_info):
        """ 
        * Retrieves the track ID
        * Given a dictionary with track info, returns the track ID or None
        * Input: {'name': name, 'year': year}
        * Output: track_id or None
        """
        track_name = track_info['name']
        release_year = int(track_info['year'])
        search_results = self.sp.search(q=f'track:{track_name} year:{release_year}', type='track', limit=1)

        if search_results['tracks']['items']:
            track_id = search_results['tracks']['items']
            return track_id
        else:
            return None

    def find_song(self, name, year):
        """
        * Searches for a song by name and release year
        * Given name and release year, returns None or a dictionary with song and audio features
        * Input: name, year
        * Output: dictionary with song info
        """
        song_data = defaultdict()
        results = self.sp.search(q='track: {} year: {}'.format(name, year), limit=1)
        if results['tracks']['items'] == []:
            return None

        results = results['tracks']['items'][0]
        track_id = results['id']
        audio_features = self.sp.audio_features(track_id)[0]

        song_data['name'] = [name]
        song_data['year'] = [year]
        song_data['explicit'] = [int(results['explicit'])]
        song_data['duration_ms'] = [results['duration_ms']]
        song_data['popularity'] = [results['popularity']]

        for key, value in audio_features.items():
            song_data[key] = value

        return pd.DataFrame(song_data).squeeze()  # Convert DataFrame to Series

    def get_song_data(self, song, spotify_data):
        """ 
        * Searches for song info in the dataset; if not found, uses find_song
        * Input: {'name': name, 'year': year} and dataset
        * Output: song information
        """
        try:
            song_data = spotify_data[(spotify_data['name'] == song['name']) 
                                    & (spotify_data['year'] == song['year'])].iloc[0]
            
            if isinstance(song_data, pd.DataFrame):
                song_data = song_data.squeeze()  # Convert DataFrame to Series
            return song_data
        except IndexError:
            return self.find_song(song['name'], song['year'])

    def get_mean_vector(self, song_list, spotify_data):
        """
        * Generates the mean vector
        * Input: list of songs and dataset
        * Output: mean vector of numerical features
        """
        song_vectors = []
        for song in song_list:
            song_data = self.get_song_data(song, spotify_data)
            if song_data is None:
                print('Warning: {} does not exist in Spotify or in database'.format(song['name']))
                continue
            song_vector = song_data[self.number_cols].values
            song_vectors.append(song_vector)

        song_matrix = np.array(list(song_vectors))
        return np.mean(song_matrix, axis=0)

    def flatten_dict_list(self, dict_list):
        """ 
        * Merges multiple dictionaries of song names and years into one dictionary
        * Input: [{'name': name, 'year': year}, ...]
        * Output: {'name': [name1, name2], 'year': [year1, year2], ...}
        """
        flattened_dict = defaultdict()
        print("dict_list", dict_list)
        for key in dict_list[0].keys():
            flattened_dict[key] = []

        for dictionary in dict_list:
            for key, value in dictionary.items():
                flattened_dict[key].append(value)
        return flattened_dict

    def recommend_songs(self, song_list, n_songs=10):
        """
        * Recommends songs
        * Input: list of songs [{'name': name, 'year': year}, ...]
        * Output: [{'name': 'name1', 'year': year1, 'artists': "artists"}, ...]
        """
        metadata_cols = ['name', 'year', 'artists']
        song_dict = self.flatten_dict_list(song_list)
        song_center = self.get_mean_vector(song_list, self.spotify_data)
        
        scaler = self.song_cluster_pipeline.steps[0][1]
        scaled_data = scaler.transform(self.spotify_data[self.number_cols])
        scaled_song_center = scaler.transform(song_center.reshape(1, -1))

        distances = cdist(scaled_song_center, scaled_data, 'cosine')
        index = list(np.argsort(distances)[:, :n_songs][0])

        rec_songs = self.spotify_data.iloc[index]
        rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])]
        return rec_songs[metadata_cols].to_dict(orient='records')
    
    def setSongClusterPipeline(self, scp):
        self.song_cluster_pipeline = scp

    def setData(self, data):
        self.spotify_data = data
