# some methods are adapted from https://github.com/plamere/spotipy/blob/master/examples/artist_discography.py

#Shows the list of all songs sung by the artist or the band
import argparse
import logging
from typing import List, Set, Tuple, Dict

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

from neo4j import (
    GraphDatabase,
    basic_auth,
)

from config import CLIENT_ID, CLIENT_SECRET, DB_URL, DB_USERNAME, DB_PASSWORD


logger = logging.getLogger('artist_discography')
logging.basicConfig(level='INFO')


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
    for album in albums:
        name = album['name'].lower()
        if name not in unique:
            logger.info('ALBUM: %s', name)
            unique_albums.add(name)
            tracks = []
            results = sp.album_tracks(album['id'])
            tracks.extend(results['items'])
            while results['next']:
                results = sp.next(results)
                tracks.extend(results['items'])
            for i, track in enumerate(tracks):
                logger.info('%s. %s', i+1, track['name'])
    return tracks

#TODO: write Cypher query to write track and associated artist info to database
def write_track_to_database(track:Dict):
    """pushes track and associated artists to database"""
    pass

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
    for artist in list_of_artists:
        for track in get_artist_tracks():
            write_track_to_database(track)


def main():
    args = get_args()
    artist = get_artist(args.artist)
    print(artist)


if __name__ == '__main__':
    client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    driver = GraphDatabase.driver(DB_URL, auth=basic_auth(DB_USERNAME, DB_PASSWORD))
    db = driver.session()
    main()