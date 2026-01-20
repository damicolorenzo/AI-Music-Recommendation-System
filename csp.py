from CSP.cspProblem import Variable, Constraint, CSP
from CSP.spotify_json import playlist_data
from CSP.searchGeneric import Searcher1
from CSP.cspSearch import Search_from_CSP

class csp:

    def __init__(self, songs):
        self.songs = songs
        Canzone = Variable('Canzone', self.get_list(self.songs))
        Playlist = Variable('Playlist',  self.in_Playlist())
        problem = CSP("problem", {Canzone, Playlist}, 
               [
                    Constraint([Canzone, Playlist], self.func)
               ]) 
        searcher = Searcher1(Search_from_CSP(problem))
        self.dict = searcher.search() 

    def get_list(self, songs):
        return_list = list()
        for song in songs:
            return_list.append(song['name'])
        return return_list
    
    def get_playlist(self, playlist):
        list_of_songs = list()
        for playlist_tracks in playlist_data[playlist]:
            list_of_songs.append(playlist_tracks)
        return list_of_songs
    
    #prende in ingresso un insieme di canzoni e ritorna il match canzone playlist prendendo le playlist dell'utente
    def in_Playlist(self):
        list_of_playlist = list()
        for playlist_name in playlist_data:
            if len(list_of_playlist) < 4:
                list_of_playlist.append(playlist_name)
            else:
                break
        return list_of_playlist
    
    def func(self, song, playlist):
        if song in self.get_playlist(playlist): #se la canzone è nella playlist
            return True
        else: 
            return False
    
    def remove_from_dict(self):
        solution = self.get_list(self.songs)
        for e in self.dict:
            for el in e.arc.to_node:
                if el.name == 'Canzone':
                    solution.remove(e.arc.to_node[el])
        solution_dict = self.songs
        for e in self.songs:        
            if e["name"] not in solution:
                solution_dict.remove(e)
        return solution_dict   