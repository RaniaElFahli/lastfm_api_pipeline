from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import analysis
from app.services.lastfmclient import LASTFMClient
from app.services.trackloader import TrackLoader
from app.services.tracktransformer import TrackTransformer
from app.services.run_pipeline import LastfmPipeline
from app.config import USERNAME, API_KEY, BASE_URL, DATABASE_URL

if __name__== "__main__":
    extractor = LASTFMClient(username=USERNAME, base_url=BASE_URL, api_key=API_KEY)
    transformer = TrackTransformer(genre_csv_path="data/genres.csv")
    loader = TrackLoader(database_url=DATABASE_URL)

    pipeline = LastfmPipeline(extractor, transformer, loader)

app = FastAPI(
    title="My musical dashboard", 
    description = "Musical dashboard based on your last.fm scrobble !", 
    version="1.0"
)

@app.get("/top-artists")

def top_artists(limit : int = 10):

    df = analysis.get_top_artists(limit)
    return df.to_dict(orient="records")

@app.get("/top-tracks")
def top_tracks(limit : int = 10): 
    df = analysis.get_top_tracks(limit)
    return df.to_dict(orient = "records")

@app.get("/listens-per-day")
def listens_per_day():
    df = analysis.get_listens_per_day()
    return df.to_dict(orient = "records")