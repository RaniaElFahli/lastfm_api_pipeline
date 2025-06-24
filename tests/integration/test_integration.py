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

load_dotenv()

@pytest.fixture
def real_lastfm_client():
   return LASTFMClient(api_key=API_KEY, base_url=BASE_URL, username=USERNAME, fetch_limit=3)

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
def test_full_pipeline_integration(real_lastfm_client):
    test_database_url = (
        f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB_test')}"
    )
    engine = create_engine(test_database_url, echo=False)

    Base.metadata.create_all(engine)

    session = Session(engine)

    from app.models import Artists, Albums, Tracks, RecentTracks, ArtistGenre, MusicGenre, AlbumGenre

    extractor = real_lastfm_client
    transformer = TrackTransformer(genre_csv_path="data/genres.csv")
    loader = TrackLoader(db=session, extractor=extractor, transformer=transformer)
    pipeline_run = LastfmPipeline(extractor=extractor, transformer=transformer, loader=loader)
    pipeline_run.run()

    assert session.query(Artists).count() > 0
    assert session.query(Albums).count() > 0
    assert session.query(Tracks).count() > 0
    assert session.query(RecentTracks).count() > 0
    assert session.query(MusicGenre).count() > 0
    assert session.query(ArtistGenre).count() > 0
    assert session.query(AlbumGenre).count() > 0

    session.close()

    Base.metadata.drop_all(engine)
    
