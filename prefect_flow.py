from prefect import flow
from app.services.run_pipeline import LastfmPipeline 
from app.services.lastfmclient import LASTFMClient
from app.services.trackloader import TrackLoader
from app.services.tracktransformer import TrackTransformer
from app.services.run_pipeline import LastfmPipeline
from app.config import API_KEY, BASE_URL, USERNAME
from app.sessions import session

@flow(log_prints=True)
def run_pipeline():
    pipeline = LastfmPipeline(
        extractor = LASTFMClient(api_key=API_KEY, base_url=BASE_URL, username=USERNAME, fetch_limit=4),
        transformer = TrackTransformer(genre_csv_path="data/genres.csv"), 
        loader = TrackLoader(db=session, extractor=extractor, transformer=transformer))
    pipeline.run()