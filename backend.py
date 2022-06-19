# some methods are adapted from https://github.com/plamere/spotipy/blob/master/examples/artist_discography.py

#Shows the list of all songs sung by the artist or the band
import logging
from typing import List, Dict
from neo4j import (
    GraphDatabase,
    basic_auth,
)


from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

from tqdm import tqdm

logger = logging.getLogger('artist-connections')
logging.basicConfig(level='INFO')

# set to true for debugging
logger.disabled = True     # set to False for debugging info to get printed to console

def get_artist(name:str) -> Dict:
    """gets dictionary object containing data of artist"""
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


def get_artist_tracks(artist:Dict) -> List[Dict]:
    """get list of artist tracks (tracks are stored as dictionaries)"""
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    logger.info('Total albums: %s', len(albums))
    unique_albums = set()  # skip duplicate albums
    tracks = []
    for album in albums:
        name = album['name'].lower()
        if name not in unique_albums:
            logger.info('ALBUM: %s', name)
            unique_albums.add(name)
            results = sp.album_tracks(album['id'])
            tracks.extend(results['items'])
            while results['next']:
                results = sp.next(results)
                tracks.extend(results['items'])
            for i, track in enumerate(tracks):
                logger.info('%s. %s', i+1, track['name'])
    return tracks


def write_track_to_database(tx, track:Dict):
    """pushes track and associated artists to database"""
    global driver

    table = str.maketrans({
    "-":  r"\-", 
    "]":  r"\]", 
    "\\": r"\\",                  
     "^":  r"\^", 
     "$":  r"\$", 
     "*":  r"\*", 
     ".":  r"\.",
     "'": r"\'",
     '"': r'\"',
     "’": r'\’'
     })

    logger.info(f"Writing to database: {str(track['name'])}-{str([artist['name'] for artist in track['artists']])}")
    command = ""

    # create track node
    command += f"""MERGE (t{track["id"]}:Track {{name:'{track["name"].translate(table)}',
    spotify_id:'{track["id"]}', link:'{track["href"]}'}})"""

    # create node for artist if it doesn't exist
    for artist in track['artists']:
        
        artist_id = "".join(artist["name"].split(" "))
        new_id = ""
        for char in artist_id:
            if char.isnumeric():
                new_id += chr(int(char)+65)    # hack to only have alphabet in id (for artists with numbers in their names)
            elif char.isalpha():
                new_id += char   # add regular characters to the new id, skip anything weird
        
        command += f"""
        MERGE ({new_id}:Artist {{name:'{artist["name"].replace("'", "")}', link:'{artist["external_urls"]["spotify"]}', id:'{artist['id']}'
        }}) """
        
        command += f"""MERGE ({new_id})-[:PERFORMED_IN]->(t{track["id"]})"""
    logger.info(command)
    tx.run(command)


#TODO
def find_collaboration_distance(artist1:str, artist2:str):
    """find min distance between two artists"""
    pass

#TODO
def find_nearby_artists(artist:str, distace:int=1):
    """find artists that are <distance> jumps away from <artist>"""
    pass


#TODO: once we have flask up and running, make driver and sp part of Flask global context instead of passing as arguments
def populate_database(list_of_artists: List[str], driver:GraphDatabase.driver, spo:spotipy.Spotify):
    """populates neo4j database with song data of artists"""
    # global driver
    global sp
    sp = spo
    for i in tqdm(range(0, len(list_of_artists)), unit=" artist", desc="Populating database"):
        artist_name = list_of_artists[i]
        artist = get_artist(artist_name)
        for track in get_artist_tracks(artist):
            # only write tracks with collaborators
            if len(track['artists']) > 1:
                with driver.session() as session:
                    session.write_transaction(write_track_to_database, track)