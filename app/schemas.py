from pydantic import BaseModel
from datetime import datetime 

class TopArtists(BaseModel):
    artist_name:str
    listen_count:int

class TopTracks(BaseModel):
    track_name:str
    artist_name:str
    listen_count:int

class TopAlbums(BaseModel):
    album_name:str
    artist_name:str
    listen_count:int

class TopGenres(BaseModel):
    genre_name:str
    listen_count:int

class Dailylisteningduration(BaseModel):
    date_time:datetime
    duration_count:float