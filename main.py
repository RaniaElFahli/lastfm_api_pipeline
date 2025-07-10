from fastapi import FastAPI
from app.sessions import session
from app.models import Artists, Tracks, Albums, ArtistGenre, RecentTracks, MusicGenre
from sqlalchemy import func, desc
from app.schemas import TopArtists, TopTracks, TopAlbums, TopGenres, Dailylisteningduration, GenreDiversity
import math

app = FastAPI(
    title="My musical dashboard", 
    description = "Musical dashboard based on your last.fm scrobble !", 
    version="1.0"
)

@app.get("/")
async def read_root():
    return {"message": "Bienvenue sur l'API Music Dashboard"}

@app.get("/top-artists", 
    response_model=TopArtists,
    summary="Top artists",
    description="Top recently streamed artists with desired limit")
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


@app.get("/top-tracks", 
    response_model=TopTracks,
    summary="Top tracks",
    description="Top recently streamed tracks with desired limit")
async def get_top_tracks(limit: int=5):

    top_tracks_query = session.query(
        Tracks.track_title, 
        Artists.artist_name,
        func.count(RecentTracks.track_id).label("tracks_listen_count")
    ).join(Tracks, Tracks.track_id == RecentTracks.track_id
    ).join(Artists, Artists.artist_id == Tracks.artist_id
    ).group_by(Tracks.track_title, Artists.artist_name
    ).order_by(desc("tracks_listen_count")).limit(limit)

    results = top_tracks_query.all()

    return [
        TopTracks(track_name=track_name, artist_name=artist_name, listen_count=tracks_listen_count)
        for track_name, artist_name, tracks_listen_count in results
    ]

@app.get("/top-albums", 
    response_model=TopAlbums,
    summary="Top streamed albums",
    description="List of top streamed albums with desired limit")
async def get_top_albums(limit: int=5):
    top_albums_query = session.query(
        Albums.album_title, 
        Artists.artist_name, 
        func.count(RecentTracks.album_id).label("albums_listen_count")
    ).join(Albums, Albums.album_id == RecentTracks.album_id
    ).join(Artists, Artists.artist_id == Albums.artist_id
    ).group_by(Albums.album_title, Artists.artist_name
    ).order_by(desc("albums_listen_count")).limit(limit)

    results = top_albums_query.all()

    return [
        TopAlbums(album_name=album_name, artist_name=artist_name, listen_count=albums_listen_count)
        for album_name, artist_name, albums_listen_count in results
    ]

@app.get("/top-genres", 
    response_model=TopGenres,
    summary="Top genres streamed",
    description="Top musical genres based on artists recently streamed with desired limit")
async def get_top_genres(limit: int=5):
    top_genres_query = session.query(
        MusicGenre.genre_name,
        func.count(RecentTracks.artist_id).label("artist_listen_count")
    ).join(ArtistGenre, ArtistGenre.artist_id == RecentTracks.artist_id
    ).join(MusicGenre, MusicGenre.genre_id == ArtistGenre.genre_id
    ).group_by(MusicGenre.genre_name
    ).order_by(desc("artist_listen_count")).limit(limit)

    results = top_genres_query.all()

    return [
           TopGenres(genre_name=genre_name, listen_count=artist_listen_count)
        for genre_name, artist_listen_count in results
    ]

@app.get("/daily-listens", 
        response_model=Dailylisteningduration,
    summary="Daily listening duration",
    description="Daily listening duration in minutes based on recent tracks")
async def get_daily_duration():
    daily_duration_query = session.query(
        func.date(RecentTracks.date_time).label("date"), 
        func.sum(Tracks.duration / 60000).label("duration_count_minutes")
    ).join(Tracks, Tracks.track_id == RecentTracks.track_id
    ).group_by("date"
    ).order_by("date")

    results = daily_duration_query.all()

    return [ Dailylisteningduration(
        date_time=date_time, duration_count=duration_count)
        for date_time, duration_count in results
    ]
@app.get("/genre-diversity", response_model=GenreDiversity,
    summary="Musical genres diversity",
    description="Entropy indicator of musical genres diversity bases on artists recently streamed")
async def get_genre_diversity():
    genres_query = session.query(
        MusicGenre.genre_name,
        func.count(RecentTracks.artist_id).label("artist_listen_count")
    ).join(ArtistGenre, ArtistGenre.artist_id == RecentTracks.artist_id
    ).join(MusicGenre, MusicGenre.genre_id == ArtistGenre.genre_id
    ).group_by(MusicGenre.genre_name) 

    results = genres_query.all()
    total_listens = sum(artist_listen_count for genre_name, artist_listen_count in results)
    entropy = 0.0

    for genre_name, artist_listen_count in results:
        probability = artist_listen_count / total_listens
        entropy -= probability * math.log(probability, 2)  # log base 2

    max_entropy = math.log(len(results), 2) if len(results) > 0 else 0
    normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0

    return [
        GenreDiversity(
            genre_diversity=normalized_entropy,
            total_listens=total_listens,
            genres=[{"genre_name": genre_name, "artist_listen_count": artist_listen_count} for genre_name, artist_listen_count in results]
        )
    ]
        