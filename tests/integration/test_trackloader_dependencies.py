from app.models import Artists, Albums, Tracks, RecentTracks

""" Testing relationships between tables while inserting data with a pre-populated postgresql test database"""

def test_get_or_create_artist_duplicates(track_loader_populated):
    existing_artist_id = track_loader_populated._get_or_create_artist(artist_name="Placebo")
    db_result = track_loader_populated.db.query(Artists).filter_by(artist_name="Placebo").first()
    assert existing_artist_id == db_result.artist_id

def test_get_or_create_album_duplicates(track_loader_populated):
    existing_album_id = track_loader_populated._get_or_create_album(album_title='Dummy', artist_name="Portishead")
    db_result = track_loader_populated.db.query(Albums).filter_by(album_title="Dummy").first()
    assert existing_album_id == db_result.artist_id

def test_get_or_create_album_dependency_insertion(track_loader_populated, mock_requests_get):
    """_get_or_create_album calls for _get_or_create_artist and inserts artist into the Artists table
    after checking for duplicates. Testing if this dependency is executed correctly"""
    mock_requests_get
    new_album_existing_artist_id = track_loader_populated._get_or_create_album(album_title='In Rainbows', artist_name='Radiohead')
    assert new_album_existing_artist_id is not None
    new_album_inserted = track_loader_populated.db.query(Albums).filter_by(album_title="In Rainbows").first()
    assert new_album_inserted.album_title == "In Rainbows"
    db_result_artist = track_loader_populated.db.query(Artists).filter_by(artist_name="Radiohead").first()
    assert new_album_inserted.artist_id == db_result_artist.artist_id

def test_get_or_create_track_dependencies_insertion(track_loader_populated, mock_requests_get):
    """ _get_or_create_track calls for both _get_or_create_artist and _get_or_create_album. It inserts 
    corresponding data into the tables Artists and Albums after checking for duplicates. Testing if these dependencies 
    are executed correctly."""

    mock_requests_get

    new_track_existing_artist_album_id = track_loader_populated._get_or_create_track(album_title='Mezzanine', artist_name='Massive Attack', 
                                                                               track_name='Angel')
    assert new_track_existing_artist_album_id is not None
    new_track_inserted = track_loader_populated.db.query(Tracks).filter_by(track_title='Angel').first()
    existing_artist = track_loader_populated.db.query(Artists).filter_by(artist_name="Massive Attack").first()
    existing_album = track_loader_populated.db.query(Albums).filter_by(album_title='Mezzanine').first()
    assert new_track_inserted.artist_id == existing_artist.artist_id    
    assert new_track_inserted.album_id == existing_album.album_id

    new_track_existing_artist_new_album_id = track_loader_populated._get_or_create_track(track_name='Weird Fishes / Arpeggi', artist_name='Radiohead', album_title='In Rainbows')
    assert new_track_existing_artist_new_album_id is not None
    new_track_existing_artist_new_album_inserted = track_loader_populated.db.query(Tracks).filter_by(track_title='Weird Fishes / Arpeggi').first()
    inserted_album = track_loader_populated.db.query(Albums).filter_by(album_title = 'In Rainbows').first()
    assert new_track_existing_artist_new_album_inserted.album_id == inserted_album.album_id

def test_load_recent_tracks_dependencies_insertion(track_loader_populated, mock_requests_get):
    """" load_recent_tracks populates the facts table (recent_tracks) and then calls for the 
     different _get_or_create methods populating the different dimension tables (Artists, Albums, Tracks) after checking 
      for duplicates. """

    mock_requests_get

    from tests.mock_api_responses import Mocklastfmresponses
    mock_recent_tracks_response = Mocklastfmresponses.mock_recent_tracks_response()
    simulate_extracted_response = mock_recent_tracks_response["recenttracks"]["track"]
    result_transformed = track_loader_populated.transformer.transform_recent_tracks(tracks_json=simulate_extracted_response)
    track_loader_populated.load_recent_tracks(tracks_data=result_transformed)
    artist = track_loader_populated.db.query(Artists).filter_by(artist_name='Radiohead').first()
    track = track_loader_populated.db.query(Tracks).filter_by(track_title='Weird Fishes / Arpeggi').first()
    album = track_loader_populated.db.query(Albums).filter_by(album_title='In Rainbows').first()
    inserted_recent_track = track_loader_populated.db.query(RecentTracks).filter_by(timestamp=1749296024).first()
    assert artist.artist_id == inserted_recent_track.artist_id
    assert track.track_id == inserted_recent_track.track_id
    assert album.album_id == inserted_recent_track.album_id

