from flask import Flask, render_template, request
from classes.ml import ML
from classes.configuration import Configuration

# Flask application configuration
app = Flask(__name__)

# Spotify API interface configuration
spotify = Configuration().getSpotify()
view = Configuration().getView()

# Initialization of the ML object that manages the model
ml = ML(spotify, view)
ml.generation()
history_track_list = []

# Home page
@app.route('/')
def index():
    return render_template('index.html')
    
# Search page
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = spotify.search(q=query, type='track')
    tracks = results['tracks']['items']
    return render_template('search.html', tracks=tracks)

# Autocomplete handling page
@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    query = request.form['query']
    results = spotify.search(q=query, type='track', limit=5)  # Limit results to 5 for demo purposes
    tracks = results['tracks']['items']
    return render_template('autocomplete.html', tracks=tracks)

# Track selection page
@app.route('/select', methods=['POST'])
def select():
    track_id = request.form['track_id']
    track_name = request.form['track_name']
    return render_template('select.html', track_id=track_id, track_name=track_name)

# Page for building the input track list
@app.route('/createList', methods=['POST'])
def createList():
    global history_track_list
    track_id = request.form['track_id']
    tpe = request.form['type']
    if tpe == "reset":
        history_track_list = []
    history_track_list.append(track_id) 
    return render_template('createList.html', track_list=history_track_list)

# Page for playing the selected track
@app.route('/play', methods=['POST'])
def play():
    track_id = request.form['track_id']
    return render_template('play.html', track_id=track_id)

# Page that generates and displays similar tracks
@app.route('/similar')
def similar():
    global history_track_list
    ml.recommend(history_track_list) 
    ml.solving()
    ml.printing()
    track_list = ml.similar_list
    ex_list = ml.removed_list
    return render_template('similar.html', similar_tracks=track_list, removed_tracks=ex_list)

if __name__ == '__main__':
    app.run(debug=True)

# To run the application, use the command:
# flask --app index run --debugger
