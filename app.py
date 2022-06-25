from backend import find_collaboration_path, save, check_artist_exists, find_direct_collaborators, count_direct_collaborations, get_artist_image_url
from config import *
from neo4j import (
    GraphDatabase,
    basic_auth,
)
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy


from flask import *
from markupsafe import Markup
app = Flask(__name__)
   
@app.route("/")
def home():
    return render_template("layout.html")

@app.route("/collaboration-path", methods=["GET", "POST"])
def collaboration_path():
    ret_text=""
    ret_data=[]
    if request.method == "POST":
        artist1 = request.form["artist1"]
        artist2 = request.form["artist2"]
        ret_text, ret_data = collaboration_path(artist1, artist2)
    return render_template("collaboration-path.html", text=ret_text, data=ret_data)


@app.route("/single-artist-collaborators", methods=["GET", "POST"])
def single_artist_collaborators():
    ret_text=""
    ret_data=[]
    artist1 = None
    if request.method == "POST":
        artist1 = request.form["artist"]
        ret_text, ret_data = direct_collaborations(artist1)
    return render_template("single-artist-collaborators.html", text=ret_text, data=ret_data, image_url=get_artist_image_url(artist1) if artist1 != None else "")



#######################################################################################################################################
### Probably smart to put these methods in another file to clean up??? idk################################

def direct_collaborations(artist:str):
    """finds all artists n hops away from artist-of-interest"""
    if not check_artist_exists(artist):
        return f"{artist} was not found in the database", []

    direct_collaborators = find_direct_collaborators(artist)
    data = []
    for collab in direct_collaborators:        
        data.append({"name":collab.get("name"), "num_collabs":count_direct_collaborations(artist, collab.get("name"))})
    return f"{artist} has directly collaborated with {len(data)} artists", data


def collaboration_path(artist1:str, artist2:str):
    """find shortest collaboration path between two artists"""
    if not check_artist_exists(artist1):
        return f"{artist1} was not found in the database", []
    
    if not check_artist_exists(artist2):
        return f"{artist2} was not found in the database", []
    
    path = find_collaboration_path(artist1, artist2)
    if path is None:
        return f"Path between {artist1} and {artist2} was not found", []

    i = 0
    data = []

    for i in range(len(path)):
        if i%2 == 0:
            data.append({"data_type":"artist", "name": path[i].get('name'), "img_url": get_artist_image_url(path[i].get('name')) })
        else:
            data.append({"data_type":"track", "id": path[i].get('spotify_id')})
    
    distance = int(len(path)/2)
    return_str = f"{artist1} is {distance} {'track' if distance == 1 else 'tracks'} away from {artist2}"
    
    return return_str, data

if __name__ == "__main__":
    client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    driver = GraphDatabase.driver(DB_URL, auth=basic_auth(DB_USERNAME, DB_PASSWORD))
    save(driver, sp)    # expose driver and spotify connection to backend.py file
    app.run(debug=True)
    