import pytest 
from unittest.mock import MagicMock,Mock
from app.services.lastfmclient import LASTFMClient
from app.services.tracktransformer import TrackTransformer
from app.services.trackloader import TrackLoader
import requests
from tests.mock_api_responses import Mocklastfmresponses
from pytest_postgresql import factories
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.models import Base

@pytest.fixture
def mock_requests_get(monkeypatch):
    def _mock_response(json_data):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = json_data
        return mock_resp

    def mock_get(url, params=None, **kwargs):
        method = params.get("method", "") if params else ""
        if method == "user.getRecentTracks":
            return _mock_response(Mocklastfmresponses.mock_recent_tracks_response())
        elif method == "album.getInfo":
            return _mock_response(Mocklastfmresponses.mock_album_info_response())
        elif method == "track.getInfo":
            return _mock_response(Mocklastfmresponses.mock_track_info_response())
        elif method == "artist.getTopTags":
            return _mock_response(Mocklastfmresponses.mock_artist_tag_response())
        elif method == "album.getTopTags":
            return _mock_response(Mocklastfmresponses.mock_album_tag_response())
        else:
            raise ValueError(f"Unhandled API method: {method}")

    monkeypatch.setattr(requests, "get", mock_get)

@pytest.fixture
def track_transformer():
   return TrackTransformer(genre_csv_path="data/genres.csv")  

@pytest.fixture
def lastfm_client(db_session_populated, track_transformer): 
   fake_logger = Mock()
   return LASTFMClient(api_key="fake_key", base_url="fake_url", username="fake_user", 
                       transformer=track_transformer, db=db_session_populated, logger=fake_logger)

@pytest.fixture
def db_session(postgresql):
    connection = f'postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}'
    engine = create_engine(connection, echo=False)
    session = Session(engine)
    Base.metadata.create_all(engine)
    yield session
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def track_loader(db_session, lastfm_client, track_transformer):
    return TrackLoader(db=db_session, extractor=lastfm_client, transformer=track_transformer)

from tests.load_orm import load_orm
postgresql_myproc = factories.postgresql_proc(load=[load_orm])
postgresql = factories.postgresql('postgresql_myproc')

@pytest.fixture
def db_session_populated(postgresql):
    connection = f'postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}'
    engine = create_engine(connection, echo=False)
    session = Session(engine)
    yield session 
    session.close()

@pytest.fixture
def track_loader_populated(db_session_populated, lastfm_client, track_transformer):
    return TrackLoader(db=db_session_populated, extractor=lastfm_client, transformer=track_transformer)