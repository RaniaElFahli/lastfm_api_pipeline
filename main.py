from fastapi import FastAPI
from app.sessions import session
from app.models import Artists, Tracks, AlbumGenre, Albums, MusicGenre, ArtistGenre, RecentTracks
from sqlalchemy import func, desc 
from app.schemas import TopArtists

app = FastAPI(
    title="My musical dashboard", 
    description = "Musical dashboard based on your last.fm scrobble !", 
    version="1.0"
)

@app.get("/")
async def read_root():
    return {"message": "Bienvenue sur l'API Music Dashboard"}

@app.get("/top-artists")
async def get_top_artists(limit: int = 5):
    top_artists_query = session.query(
        Artists.artist_name,
        func.count(RecentTracks.artist_id).label('artist_listen_count')
    ).join(Artists, Artists.artist_id == RecentTracks.artist_id
    ).group_by(Artists.artist_name
    ).order_by(desc('artist_listen_count')).limit(limit)

    results = top_artists_query.all()
    return [
        TopArtists(artist_name=artist_name, listen_count=artist_listen_count)
        for artist_name, artist_listen_count in results
    ]

