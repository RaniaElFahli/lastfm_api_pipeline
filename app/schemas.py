from pydantic import BaseModel

class TopArtists(BaseModel):
    artist_name:str
    listen_count:int

class TopTracks(BaseModel):
    track_name:str
    artist_name:str
    listen_count:int