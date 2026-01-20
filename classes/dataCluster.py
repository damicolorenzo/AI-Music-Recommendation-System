import warnings
warnings.filterwarnings("ignore", "\nPyarrow", DeprecationWarning)

import pandas as pd
import numpy as np
import plotly.express as px 
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans 
from sklearn.preprocessing import StandardScaler 
from sklearn.pipeline import Pipeline 


class dataCluster: 
    """
    Handles data preprocessing, clustering, and visualization
    for both song-level and genre-level datasets.
    """

    # Load datasets once at class level to avoid repeated I/O operations
    data = pd.read_csv("./dataset/data.csv")
    genre_data = pd.read_csv("./dataset/data_by_genres.csv")

    def __init__(self, view=False):
        """
        Initializes clustering pipelines.
        If 'view' is True, data visualizations are displayed.
        """
        if view:
            # Genre clustering and visualization
            X = self.method1()
            self.method2(view, X)

            # Song clustering and visualization
            Y, song_cluster_pipeline = self.method3()
            self.method4(view, Y)

            self.song_cluster_pipeline = song_cluster_pipeline
        else:
            # Only build the song clustering model without visualization
            Y, song_cluster_pipeline = self.method3()
            self.song_cluster_pipeline = song_cluster_pipeline

    def method1(self):
        """
        Performs clustering on genre-level numerical features
        using StandardScaler + KMeans.
        """
        cluster_pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('kmeans', KMeans(n_clusters=10))
        ])

        # Select only numerical features
        X = self.genre_data.select_dtypes(np.number)

        # Fit clustering model and assign cluster labels
        cluster_pipeline.fit(X)
        self.genre_data['cluster'] = cluster_pipeline.predict(X)

        return X

    def method2(self, view, X):
        """
        Applies t-SNE to reduce genre feature dimensionality
        for visualization purposes.
        """
        tsne_pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('tsne', TSNE(n_components=2, verbose=1))
        ])

        # Compute 2D embedding
        genre_embedding = tsne_pipeline.fit_transform(X)

        # Create dataframe for visualization
        projection = pd.DataFrame(columns=['x', 'y'], data=genre_embedding)
        projection['genres'] = self.genre_data['genres']
        projection['cluster'] = self.genre_data['cluster']

        # Scatter plot of genre clusters
        fig = px.scatter(
            projection,
            x='x',
            y='y',
            color='cluster',
            hover_data=['x', 'y', 'genres']
        )

        if view:
            fig.show()

    def method3(self):
        """
        Builds the main song clustering pipeline using
        StandardScaler and KMeans.
        """
        song_cluster_pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('kmeans', KMeans(n_clusters=20, verbose=False))
        ], verbose=False)

        # Select numerical song features
        Y = self.data.select_dtypes(np.number)

        # Fit clustering model and assign cluster labels
        song_cluster_pipeline.fit(Y)
        song_cluster_labels = song_cluster_pipeline.predict(Y)
        self.data['cluster_label'] = song_cluster_labels

        return Y, song_cluster_pipeline

    def method4(self, view, Y):
        """
        Uses PCA to project song features into 2D space
        for cluster visualization.
        """
        pca_pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('PCA', PCA(n_components=2))
        ])

        # Compute 2D PCA embedding
        song_embedding = pca_pipeline.fit_transform(Y)

        # Create dataframe for visualization
        projection = pd.DataFrame(columns=['x', 'y'], data=song_embedding)
        projection['title'] = self.data['name']
        projection['cluster'] = self.data['cluster_label']

        # Scatter plot of song clusters
        fig = px.scatter(
            projection,
            x='x',
            y='y',
            color='cluster',
            hover_data=['x', 'y', 'title']
        )

        if view:
            fig.show()

    def getSongClusterPipeline(self):
        """
        Returns the trained song clustering pipeline.
        """
        return self.song_cluster_pipeline
    
    def getData(self):
        """
        Returns the song dataset with cluster labels.
        """
        return self.data
