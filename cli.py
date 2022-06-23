"""CLI to perform same queries we'll do on website and output to terminal"""


from backend import find_collaboration_path, save, check_artist_exists, find_direct_collaborators
from config import *
from neo4j import (
    GraphDatabase,
    basic_auth,
)
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys


def collaboration_path():
    """find shortest collaboration path between two artists"""
    artist1 = input("Name of artist 1: ")
    artist2 = input("Name of artist 2: ")

    if not check_artist_exists(artist1):
        print(f"{artist1} was not found in the database")
        return
    
    if not check_artist_exists(artist2):
        print(f"{artist2} was not found in the database")
        return
    
    path = find_collaboration_path(artist1, artist2)
    if path is None:
        print(f"Path between {artist1} and {artist2} was not found")
        return
    i = 0
    for i in range(len(path)):
        label = "Artist: " if i%2==0 else "Track: "
        print(label, path[i].get('name'))
        if i != len(path) - 1:
            print("   |\n"*2+"   |")
            print("   v")
    
    distance = int(len(path)/2)
    print(f"{artist1} is {distance} {'track' if distance == 1 else 'tracks'} away from {artist2}")
            

def direct_collaborations():
    """finds all artists n hops away from artist-of-interest"""
    artist = input("Name of artist: ")
    if not check_artist_exists(artist):
        print(f"{artist} was not found in the database")
        return

    direct_collaborators = find_direct_collaborators(artist)
    print("Directly connected artists: ")
    for artist in direct_collaborators:
        print(artist.get("name"))
    return


def main():
    global sp, driver
    save(driver, sp)    # expose driver and spotify connection to backend.py file
    while True:
        print()
        x = input("""Options\n1 - Find collaboration path between two artists\n2 - Direct collaborations of single artist\n3 - Exit\nYour choice: """)
        print()
        if x == "1":
            collaboration_path()
        elif x == "2":
            direct_collaborations()
        elif x == "3":
            sys.exit(0)
        else:
            print("Invalid, please either input either of the following characters: [1,2,3]")


if __name__ == '__main__':
    client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    driver = GraphDatabase.driver(DB_URL, auth=basic_auth(DB_USERNAME, DB_PASSWORD))

    main()