"""script to populate Neo4j database"""
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from neo4j import (
    GraphDatabase,
    basic_auth,
)

from config import CLIENT_ID, CLIENT_SECRET, DB_URL, DB_USERNAME, DB_PASSWORD
from backend import populate_database

FILENAME = "artist_names.txt"
NUM_ARTISTS = 500   # number of artists to get data for
# Note that there are 1000 names in the artist_names.txt folder

def main():
    global driver   # using global variable for db now, switch to Flask g later

    # Get list of artist names from the stored .txt file
    artist_list_file = open(FILENAME, "r")
    file_contents = artist_list_file.read()
    artist_list = file_contents.split("\n")
    artist_list = artist_list[:NUM_ARTISTS] # last element is a blank line

    populate_database(artist_list, driver, sp)


if __name__ == '__main__':
    client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    driver = GraphDatabase.driver(DB_URL, auth=basic_auth(DB_USERNAME, DB_PASSWORD))
    main()