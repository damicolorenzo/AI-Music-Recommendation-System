# AI Music Recommendation System
An AI-powered music recommendation system that suggests songs similar to a given input track (or set of tracks), combining Machine Learning and Constraint Satisfaction Problems (CSP).

The project includes a web interface built with Flask and integrates with the Spotify Web API.

## Developed as a final project for Fundamentals and Applications of Artificial Intelligence.

## Project Overview
The goal of this project is to build a personal assistant for song prediction.
Given one or more song titles as input, the system returns a finite set of similar songs, filtered according to user-specific constraints.

The recommendation process consists of two main components:

1. Machine Learning module
  - Clusters songs based on numerical and audio features
  - Finds songs that are most similar using cosine distance

2. Constraint Satisfaction Problem (CSP) module
  - Applies constraints to refine recommendations
  - Avoids recommending songs already present in the user’s Spotify playlists

## Technologies & Libraries
- Python
- Flask – web interface
- Scikit-learn – ML pipelines (StandardScaler, KMeans)
- Pandas / NumPy – data handling
- Plotly – data visualization
- Spotify Web API – song metadata and user playlists

## Project Structure
```
ProgettoAI/
│
├── classes/
│   ├── CSP/                  # CSP algorithms and utilities
│   ├── csp.py                # CSP problem definition
│   ├── datacluster.py        # Data analysis & clustering
│   ├── ml.py                 # Machine learning logic
│   ├── recommender.py        # Recommendation engine
│   └── configuration.py     # Spotify API configuration
│
├── dataset/                  # Music datasets
│
├── templates/                # HTML templates (Flask)
│
├── index.py                  # Main Flask application
│
├── config.txt                # Spotify API credentials
└── README.md
```

## Setup & Installation
1. Clone the repository
git clone https://github.com/damicolorenzo/ProgettoAI.git
cd ProgettoAI

2. Install dependencies
pip install -r requirements.txt
(If requirements.txt is missing, install manually: flask, pandas, numpy, scikit-learn, plotly, spotipy)

## Spotify API Configuration
Create a file called config.txt in the project root with the following format:
```
{
  "client_id": "YOUR_SPOTIFY_CLIENT_ID",
  "client_secret": "YOUR_SPOTIFY_CLIENT_SECRET",
  "view": false
}
```

## How to get Spotify credentials:
1. Go to Spotify for Developers
2. Create a new application
3. Copy Client ID and Client Secret
4. Paste them into config.txt

## Run the Application
Start the Flask server with:
```
flask --app index run --debugger
```

After a few seconds, a local URL will appear in the terminal.
Open it in your browser to access the web interface.

## How It Works
1. Search for a song by title
2. Select the correct track from Spotify results
3. Optionally add more input songs
4. Generate recommendations based on:
  . KMeans clustering
  . Cosine similarity
  . User playlist constraints (CSP)

Songs that violate constraints are still shown but visually highlighted.

## Data Analysis & Visualization
When "view": true in config.txt, the system performs data analysis and visualizations:

- StandardScaler – feature normalization
- KMeans – clustering songs and genres
- t-SNE – nonlinear dimensionality reduction
- PCA – linear dimensionality reduction

These help explore dataset structure and clustering behavior.

## Recommendation Logic
- Songs are represented as numerical feature vectors
- Features are standardized (mean = 0, std = 1)
- Similarity is computed using cosine distance
- The top N closest songs are selected
- Input songs are excluded from recommendations

## Limitations
- Recommendations depend on the size and quality of the dataset
- Output is deterministic (same input → same output)
- No real-time model retraining

## Author
Lorenzo D’Amico
Final Project – June 2024
