from app.models import Artists, Albums, Tracks, RecentTracks, MusicGenre, ArtistGenre, AlbumGenre
from tests.mock_api_responses import Mocklastfmresponses

def test_get_or_create_artist_insertion(track_loader):
    track_loader._get_or_create_artist(artist_name="Radiohead")
    test_result = track_loader.db.query(Artists).filter_by(artist_name="Radiohead").first()
    assert test_result.artist_name == "Radiohead"
    assert test_result.artist_id is not None

def test_get_or_create_album_insertion(track_loader, mock_requests_get):
    mock_requests_get
    track_loader._get_or_create_album(album_title="In Rainbows", artist_name="Radiohead")
    test_result = track_loader.db.query(Albums).filter_by(album_title="In Rainbows").first()
    assert test_result.album_title == "In Rainbows"
    assert test_result.album_id is not None

def test_get_or_create_track_insertion(track_loader, mock_requests_get):
    mock_requests_get
    track_loader._get_or_create_track(album_title="In Rainbows", track_name='Weird Fishes / Arpeggi', artist_name='Radiohead')
    test_result = track_loader.db.query(Tracks).filter_by(track_title='Weird Fishes / Arpeggi').first()
    assert test_result.track_title == 'Weird Fishes / Arpeggi'
    assert test_result.track_id is not None

def test_load_recent_tracks_insertion(track_loader, mock_requests_get):
    mock_requests_get
    mock_recent_tracks_response = Mocklastfmresponses.mock_recent_tracks_response()
    simulate_extracted_response = mock_recent_tracks_response["recenttracks"]["track"]
    result_transformed = track_loader.transformer.transform_recent_tracks(tracks_json=simulate_extracted_response)
    track_loader.load_recent_tracks(tracks_data=result_transformed)
    test_result = track_loader.db.query(RecentTracks).first()
    assert test_result.listen_id is not None
    assert test_result.timestamp == 1749296024

def test_get_or_create_music_genre_insertion(track_loader, mock_requests_get):
    mock_requests_get
    track_loader._get_or_create_music_genre(genre_name='rock')
    test_result = track_loader.db.query(MusicGenre).filter_by(genre_name='rock').first()
    assert test_result.genre_id is not None
    assert test_result.genre_name == 'rock'

def test_load_artist_genres_insertion(track_loader, mock_requests_get):
    mock_requests_get
    track_loader.load_artist_genres(artist_name='Radiohead')
    test_result = track_loader.db.query(ArtistGenre).all()
    assert all(ag.genre_id is not None for ag in test_result)
    artist = track_loader.db.query(Artists).filter_by(artist_name='Radiohead').first()
    assert artist.artist_id is not None
    assert all(ag.artist_id == artist.artist_id for ag in test_result )


def test_load_album_genres_insertion(track_loader, mock_requests_get):
    mock_requests_get
    track_loader.load_album_genres(album_title='In Rainbows', artist_name='Radiohead')
    test_result = track_loader.db.query(AlbumGenre).all()
    assert all(ag.genre_id is not None for ag in test_result)
    album = track_loader.db.query(Albums).filter_by(album_title='In Rainbows').first()
    assert album.album_id is not None
    assert all(ag.album_id == album.album_id for ag in test_result )
