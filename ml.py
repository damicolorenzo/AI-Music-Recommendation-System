from dataCluster import dataCluster
from recommender import Recommender
from csp import csp

class ML:

    def __init__(self, spotify):
        self.d = dataCluster()
        self.r = Recommender(spotify)
        self.similar_list = list()
        self.songs = []
        
    def generation(self):
        self.r.setSongClusterPipeline(self.d.getSongClusterPipeline())
        self.r.setData(self.d.getData()) 
    
    def solving(self):
        c = csp(self.songs)
        self.songs = c.remove_from_dict()
        
    def recommend(self, track):
        self.songs = []
        self.songs = self.r.recommend_songs(self.r.get_track_info(track)) 
    
    def printing(self):
        self.similar_list = []
        for e in self.songs:
            if self.r.get_track_id(e) is not None:
                self.similar_list.append(self.r.get_track_id(e)[0])