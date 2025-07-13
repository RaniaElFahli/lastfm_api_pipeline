import logging 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

from prefect import flow, get_run_logger, task
from app.services.lastfmclient import LASTFMClient
from app.services.trackloader import TrackLoader
from app.services.tracktransformer import TrackTransformer
from app.config import API_KEY, BASE_URL, USERNAME
from app.sessions import session
from prefect_email import email_send_message, EmailServerCredentials
from prefect.context import get_run_context
from prefect.states import State

def notify_flow_run_state(state: State):
    credentials = EmailServerCredentials.load("email-credentials")
    context = get_run_context()
    flow_run_name = context.flow_run.name
    run_id = context.flow_run.id
    if isinstance(state, State.Completed):
        subject = f"Flow {flow_run_name} completed successfully"
        message = f"Flow run {flow_run_name} with ID {run_id} has completed successfully."
    elif isinstance(state, State.Failed):
        subject = f"Flow {flow_run_name} failed"
        message = f"Flow run {flow_run_name} with ID {run_id} has failed. Please check the logs for more details."
    
    email_send_message(
        subject=subject,
        message=message,
        email_server_credentials=credentials
    )


def make_loader(logger):
    extractor = LASTFMClient(api_key=API_KEY, base_url=BASE_URL, username=USERNAME, fetch_limit=4, logger=logger)
    transformer = TrackTransformer(genre_csv_path="data/genres.csv")
    loader = TrackLoader(db=session, extractor=extractor, transformer=transformer, logger=logger)
    return loader

@task(log_prints=True, name="fetch_lastfm_data")
def fetch_lastfm_data():
    logger = get_run_logger()
    extractor = LASTFMClient(api_key=API_KEY, base_url=BASE_URL, username=USERNAME, fetch_limit=4, logger=logger)
    logger.info(f"Fetching recent tracks with limit : {extractor.fetch_limit}")
    logger.info(f"Fetching recent tracks for user : {extractor.username}")
    return extractor.fetch_recent_tracks()

@task(log_prints=True, name="transform_lastfm_data")
def transform_lastfm_data(tracks_json):
    logger = get_run_logger()
    logger.info("Transforming recent tracks data")
    transformer = TrackTransformer(genre_csv_path="data/genres.csv")
    return transformer.transform_recent_tracks(tracks_json)

@task(log_prints=True, name="load_lastfm_tracks_data")
def load_tracks(tracks_data):
    logger = get_run_logger()
    logger.info("Loading recent tracks into the database")
    loader = make_loader(logger)
    return loader.load_recent_tracks(tracks_data=tracks_data)

@task(log_prints=True, name="load_lastfm_artist_album_genres_data")
def load_artist_album_genres(tracks_data):
    logger = get_run_logger()
    logger.info("Loading artist and album genres into the database")
    loader = make_loader(logger)
    for track in tracks_data: 
          artist = track['artist']
          album = track['album']
          loader.load_artist_genres(artist_name=artist)
          loader.load_album_genres(artist_name=artist, album_title=album)

@flow(log_prints=True, name="run_pipeline_lastfm", on_exit=notify_flow_run_state)
def lastfm_etl():
    logger = get_run_logger()
    logger.info("Starting Last.fm ETL pipeline")
    tracks_json = fetch_lastfm_data()
    tracks_data = transform_lastfm_data(tracks_json)
    load_tracks(tracks_data)
    load_artist_album_genres(tracks_data)
    logger.info("Last.fm ETL pipeline completed successfully")

if __name__ == "__main__":
    lastfm_etl.from_source(
        source="https://github.com/RaniaElFahli/lastfm_api_pipeline.git", 
        entrypoint="prefect_flow.py:lastfm_etl"
    ).serve(
        name="deploy-lastfm-etl"
    )