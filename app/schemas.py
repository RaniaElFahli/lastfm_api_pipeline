from pydantic import BaseModel

class TopArtists(BaseModel):
    artist_name:str
    listen_count:int