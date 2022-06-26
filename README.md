# musician-connections
Analyze collaborations between famous musicians

<!-- [![Musician-Collaborations](https://img.youtube.com/vi/KpuqFtTYpeQ/0.jpg)](https://www.youtube.com/watch?v=KpuqFtTYpeQ)
 -->



![Direct Collaborations](https://github.com/saahithjanapati/musician-connections/blob/main/screenshot.png?raw=true)

![Collaboration Path](https://github.com/saahithjanapati/musician-connections/blob/main/screenshot2.png?raw=true)

<!-- [https://github.com/saahithjanapati/musician-connections/blob/main/screenshot.png?raw=true]
 -->
[Link to YouTube Video](https://www.youtube.com/watch?v=KpuqFtTYpeQ)

[Link to Heroku Deployment](musician-connections.herokuapp.com/)

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

### Run app.py
Start the Flask server by running
```
python app.py
```


