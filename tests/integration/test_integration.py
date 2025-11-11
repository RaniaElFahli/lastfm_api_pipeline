from sqlalchemy.orm import Session
from sqlalchemy import create_engine 
from app.models import Base
from dotenv import load_dotenv
import os 
from app.services.lastfmclient import LASTFMClient
from app.services.trackloader import TrackLoader
from app.services.tracktransformer import TrackTransformer
from app.services.run_pipeline import LastfmPipeline
from app.config import API_KEY, BASE_URL, USERNAME
import pytest
import logging 
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

load_dotenv()

@pytest.fixture
def test_db_session():
    test_database_url = (
        f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB_test')}"
    )
    engine = create_engine(test_database_url, echo=False)
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def real_transformer():
    return TrackTransformer(genre_csv_path="data/genres.csv")

@pytest.fixture
def real_lastfm_client(real_transformer, test_db_session):
   return LASTFMClient(api_key=API_KEY, base_url=BASE_URL, username=USERNAME,
                    transformer=real_transformer, db=test_db_session, logger=logger)

def test_lastfmapi_recent_tracks(real_lastfm_client):
   results = real_lastfm_client.fetch_recent_tracks()
   assert isinstance(results, list)
   assert all(isinstance(result, dict) for result in results)
   assert len(results) > 0

@pytest.mark.dependency(name="test_status_code")
def test_check_call_lastfm_status_code(real_lastfm_client):
    params = {
            "method" : "user.getRecentTracks", 
            "user" : USERNAME, 
            "api_key" : API_KEY, 
            "format" : "json",
            "limit": 2
        } 
    code = real_lastfm_client.check_call_lastfm_client_code(url=BASE_URL, params=params)
    assert code == 200

@pytest.mark.dependency(depends=["test_status_code"])
def test_full_pipeline_integration(real_lastfm_client, real_transformer, test_db_session):

    from app.models import Artists, Albums, Tracks, RecentTracks, ArtistGenre, MusicGenre, AlbumGenre

    extractor = real_lastfm_client
    transformer = real_transformer
    loader = TrackLoader(db=test_db_session, extractor=extractor, transformer=transformer)
    pipeline_run = LastfmPipeline(extractor=extractor, transformer=transformer, loader=loader)
    pipeline_run.run()

    assert test_db_session.query(Artists).count() > 0
    assert test_db_session.query(Albums).count() > 0
    assert test_db_session.query(Tracks).count() > 0
    assert test_db_session.query(RecentTracks).count() > 0
    assert test_db_session.query(MusicGenre).count() > 0
    assert test_db_session.query(ArtistGenre).count() > 0
    assert test_db_session.query(AlbumGenre).count() > 0
    
