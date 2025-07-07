logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

from prefect import flow
from app.services.run_pipeline import LastfmPipeline 
from app.services.lastfmclient import LASTFMClient
from app.services.trackloader import TrackLoader
from app.services.tracktransformer import TrackTransformer
from app.config import API_KEY, BASE_URL, USERNAME
import app.config
from app.sessions import session
import logging 

@flow(log_prints=True, name="run_pipeline_lastfm")
def lastfm_etl():
    extractor = LASTFMClient(api_key=API_KEY, base_url=BASE_URL, username=USERNAME, fetch_limit=4)
    transformer = TrackTransformer(genre_csv_path="data/genres.csv")
    loader = TrackLoader(db=session, extractor=extractor, transformer=transformer)
    pipeline = LastfmPipeline(
        extractor = extractor, 
        transformer = transformer,
        loader = loader)
    pipeline.run()

if __name__ == "__main__":
    lastfm_etl.serve(
        name="deploy-lastfm-etl"
    )