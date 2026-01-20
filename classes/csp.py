from classes.CSP.cspProblem import Variable, Constraint, CSP
from classes.CSP.spotify_json import playlist_data
from classes.CSP.searchGeneric import Searcher1
from classes.CSP.cspSearch import Search_from_CSP

class csp:

    def __init__(self, songs):
        """
        Creates a CSP object and initializes the dictionary
        that contains the CSP result.
        """
        self.songs = songs
        Song = Variable('Song', self.get_list(self.songs))
        Playlist = Variable('Playlist', self.in_playlist())
        problem = CSP("problem", {Song, Playlist}, 
               [
                    Constraint([Song, Playlist], self.func)
               ]) 
        searcher = Searcher1(Search_from_CSP(problem))
        self.dict = searcher.search() 

    def get_list(self, songs):
        """
        * Extracts song names
        * Given a list of objects, returns a list of song titles
        * Input:  [{'name': 'value1', ...}, ...]
          Output: ['name1', 'name2', ...]
        """
        return_list = list()
        for song in songs:
            return_list.append(song['name'])
        return return_list
    
    def get_playlist(self, playlist):
        """
        * Extracts songs from a playlist
        * Given a playlist name, returns a list of songs
          (tracks contained in the playlist)
        """
        list_of_songs = list()
        for playlist_tracks in playlist_data[playlist]:
            list_of_songs.append(playlist_tracks)
        return list_of_songs
    
    # Takes a set of songs as input and returns the song–playlist matches
    # using the user's playlists
    def in_playlist(self):
        """ 
        Retrieves the user's playlists
        """
        list_of_playlist = list()
        for playlist_name in playlist_data:
                list_of_playlist.append(playlist_name)
        return list_of_playlist
    
    def func(self, song, playlist):
        """
        * CSP utility function
        * Checks whether a song is contained in a playlist
        """
        if song in self.get_playlist(playlist): 
            return True
        else: 
            return False
    
    def remove_from_dict(self):
        """ 
        * Removes songs from the song object dictionary
        * Song dictionary format: [{'name': 'value1', ...}, ...]
        * Returns a pair of objects (valid songs and removed songs)
        """
        solution = self.get_list(self.songs)
        removed_songs_names = []
        for e in self.dict:
            for el in e.arc.to_node:
                if el.name == 'Song':
                    solution.remove(e.arc.to_node[el])
        solution_dict = self.songs
        for e in self.songs:        
            if e["name"] not in solution:
                solution_dict.remove(e)
                removed_songs_names.append(e)
        return solution_dict, removed_songs_names   
