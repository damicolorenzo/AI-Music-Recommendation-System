from classes.dataCluster import dataCluster
from classes.recommender import Recommender
from classes.csp import csp

class ML:

    def __init__(self, spotify, view):
        self.d = dataCluster(view)
        self.r = Recommender(spotify)
        self.similar_list = list()
        self.songs = []
        self.removed_songs = []
        
    def generation(self):
        """
        Method that establishes the connection between the dataCluster,
        which manages the datasets, and the Recommender, which manages
        the recommendation model.
        """
        self.r.setSongClusterPipeline(self.d.getSongClusterPipeline())
        self.r.setData(self.d.getData()) 
    
    def solving(self):
        """
        Method that creates a CSP instance and retrieves both the CSP
        solution and the discarded elements.
        """
        c = csp(self.songs)
        self.songs, self.removed_songs = c.remove_from_dict()
        
    def recommend(self, track_list):
        """
        Method that generates song recommendations given an input track
        or a list of track identifiers.
        """
        self.songs = []
        temp_list = []
        if type(track_list) == 'string':
            track_list = [].append(track_list)
        for e in track_list:
            temp_list.append(self.r.get_track_info(e))
            print(temp_list)
        self.songs = self.r.recommend_songs(temp_list) 
    
    def printing(self):
        """
        Converts a list of recommended songs from metadata objects
        to a list of Spotify track identifiers.
        """
        self.similar_list = []
        for e in self.songs:
            if self.r.get_track_id(e) is not None:
                x = self.r.get_track_id(e)[0]
                self.similar_list.append(x)
            else:
                e.update({'album': None})
                self.similar_list.append(e)

        self.removed_list = []
        for e in self.removed_songs:
            if self.r.get_track_id(e) is not None:
                self.removed_list.append(self.r.get_track_id(e)[0])
