# artist-connections
Analyze collaborations between famous music artists

## Known Issues / Things to Fix
- Track titles are getting messed up with backslashes before punctuation symbols
- Artist name inputs are case sensitive (will probably be annoying in the actual app).... Maybe we could have an autocomplete feature??? 
- Some artists names are repeated in the database (for some reason, it's picking up users with the same names as famous artists)

## Running locally

### Neo4j Database 
Download [Neo4j desktop](https://neo4j.com/download/) and create a database. It can be in a new or preexisting project.

Note the database uri/url, password, and username. 


### Spotify API Credentials
If you don't have Spotify API credentials, go to this [site](https://developer.spotify.com/dashboard/applications), make an application, and store the client id and client secret.


### config.py file
Fill out the config.py file with the information from previous two sections.
```
CLIENT_ID = ""
CLIENT_SECRET = ""


DB_PASSWORD = ""
DB_URL = ""
DB_USERNAME = ""
```


### Install dependecies
```
pip install -r requirements.txt
```

### Populate database
Run the populate_database.py script to get data for artists and add it to the Neo4j graph database. This took me about an hour for 500 artists.

```
python populate_database.py
```



[Planning Doc](https://docs.google.com/document/d/11QZeygbCeInZviqpyPku9D_t70USBIeeOcIpqs62yPA/edit?usp=sharing)
