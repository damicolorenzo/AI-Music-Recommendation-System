import warnings
warnings.filterwarnings("ignore", "\nPyarrow", DeprecationWarning)
import pandas as pd
import numpy as np
import plotly.express as px 
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans #K-means è un algoritmo di analisi dei gruppi partizionale che permette di suddividere un insieme di oggetti in k gruppi sulla base dei loro attributi
from sklearn.preprocessing import StandardScaler #Normalizzazione e standardizzazione di attributi/variabili/colonne (media = 0 e deviazione standard = 1)
from sklearn.pipeline import Pipeline #The purpose of the pipeline is to assemble several steps that can be cross-validated together while setting different parameters.

class dataCluster: 

    data = pd.read_csv("./dataset/data.csv")
    genre_data = pd.read_csv("./dataset/data_by_genres.csv")

    def __init__(self):
        """ self.cluster_pipeline = Pipeline([('scaler', StandardScaler()), ('kmeans', KMeans(n_clusters=14, n_init=10))])
        X = self.genre_data.select_dtypes(np.number)
        self.cluster_pipeline.predict(X)
        self.genre_data['cluster'] = self.cluster_pipeline.fit(X)
        
        tsne_pipeline = Pipeline([('scaler', StandardScaler()), ('tsne', TSNE(n_components=2, verbose=1))])
        genre_embedding = tsne_pipeline.fit_transform(X)
        projection = pd.DataFrame(columns=['x', 'y'], data=genre_embedding)
        projection['genres'] = self.genre_data['genres']
        projection['cluster'] = self.genre_data['cluster']

        fig = px.scatter(
            projection, x='x', y='y', color='cluster', hover_data=['x', 'y', 'genres'])
        #fig.show()  """

        self.song_cluster_pipeline = Pipeline([('scaler', StandardScaler()), 
                                        ('kmeans', KMeans(n_clusters=20, n_init=20, 
                                        verbose=False)) #n_clusters = 20 numero di cluster creati, verbose = False: non stampa informazioni extra
                                        ], verbose=False)

        Y = self.data.select_dtypes(np.number) #This selects only the columns in the DataFrame data that have numerical data types
        #number_cols = list(X.columns) #the song_cluster_pipeline is trained and ready to be used for making predictions or further analysis.
        self.song_cluster_pipeline.fit(Y)
        song_cluster_labels = self.song_cluster_pipeline.predict(Y)
        self.data['cluster_label'] = song_cluster_labels

        pca_pipeline = Pipeline([('scaler', StandardScaler()), ('PCA', PCA(n_components=2))])
        song_embedding = pca_pipeline.fit_transform(Y)
        projection = pd.DataFrame(columns=['x', 'y'], data=song_embedding)
        projection['title'] = self.data['name']
        projection['cluster'] = self.data['cluster_label']

        fig = px.scatter(
            projection, x='x', y='y', color='cluster', hover_data=['x', 'y', 'title'])
        #fig.show()

    def getSongClusterPipeline(self):
        return self.song_cluster_pipeline
    
    def getData(self):
        return self.data
    