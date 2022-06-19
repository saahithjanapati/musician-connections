# some methods are adapted from https://github.com/plamere/spotipy/blob/master/examples/artist_discography.py

#Shows the list of all songs sung by the artist or the band
import argparse
import logging
from typing import List, Set, Tuple, Dict
import re


from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

from neo4j import (
    GraphDatabase,
    basic_auth,
)

from config import CLIENT_ID, CLIENT_SECRET, DB_URL, DB_USERNAME, DB_PASSWORD

logger = logging.getLogger('artist-connections')
logging.basicConfig(level='INFO')

# set to true for debugging
logger.disabled = False     # set to False for debugging info to get printed to console


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
    logger.info(f"Writing to database: {str(track['name'])}-{str([artist['name'] for artist in track['artists']])}")
    command = ""

    # create track node (hopefully it's unique)
    command += f"""MERGE (t{track["id"]}:Track {{name:'{track["name"].replace("'", "")}',
    spotify_id:'{track["id"]}', link:'{track["href"]}'}})"""


    # create node if it doesn't exist
    for artist in track['artists']:
        artist_id = "".join(artist["name"].split(" "))
        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

        new_id = ""
        for char in artist_id:
            if char.isnumeric():
                new_id += chr(int(char)+65)    # hack to only have alphabet in id (for artists with numbers in their names)
            elif char in punc:
                continue
            else:
                new_id += char
        
        command += f"""
        MERGE ({new_id}:Artist {{name:'{artist["name"]}', link:'{artist["external_urls"]["spotify"]}', id:'{artist['id']}'
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


def populate_database(list_of_artists: List[str]):
    """populates neo4j database with song data of artists"""
    global driver

    for artist_name in list_of_artists:
        artist = get_artist(artist_name)
        for track in get_artist_tracks(artist):
            logger.info(artist)
            with driver.session() as session:
                session.write_transaction(write_track_to_database, track)
                # write_track_to_database(track)
            # print(track)
        # print(artist)


def main():
    TEST_ARTIST_LIST = ["Drake"]
    populate_database(TEST_ARTIST_LIST)


if __name__ == '__main__':
    global db,driver   # using global variable for db now, switch to Flask g later
    
    client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    driver = GraphDatabase.driver(DB_URL, auth=basic_auth(DB_USERNAME, DB_PASSWORD))
    # db = driver.session()
    main()
    # db.close()  # close connection