import pytest

def test_fetch_recent_tracks_output_type(mock_requests_get, lastfm_client):
    
    mock_requests_get

    recent_tracks = lastfm_client.fetch_recent_tracks()
    assert isinstance(recent_tracks, list)
    assert all(isinstance(track, dict) for track in recent_tracks)
 
def test_fetch_info_data_album_output_type(mock_requests_get, lastfm_client):

    mock_requests_get

    info_data_album = lastfm_client.fetch_info_data("album", album="In Rainbows", artist="Radiohead")
    assert isinstance(info_data_album, dict)

def test_fetch_info_data_track_output_type(mock_requests_get, lastfm_client):

    mock_requests_get

    info_data_track = lastfm_client.fetch_info_data("album", track="Weird Fishes / Arpeggi", artist="Radiohead")
    assert isinstance(info_data_track, dict)

def test_fetch_info_data_invalid_kwargs_raise_error(mock_requests_get, lastfm_client):
    mock_requests_get
    with pytest.raises(ValueError):
        lastfm_client.fetch_info_data(type="album", unknown_kwarg="oops")

def test_fetch_top_tags_album_output_type(mock_requests_get, lastfm_client):

    mock_requests_get

    album_tags = lastfm_client.fetch_top_tags('album', album="In Rainbows", artist="Radiohead")
    assert isinstance(album_tags, list)
    assert all(isinstance(tag, str) for tag in album_tags)

def test_fetch_top_tags_artist_output_type(mock_requests_get, lastfm_client):
       
    mock_requests_get

    artist_tags = lastfm_client.fetch_top_tags(type="artist", artist="Radiohead")
    assert isinstance(artist_tags, list)
    assert all(isinstance(tag, str) for tag in artist_tags)

def test_fetch_info_data_invalid_type_raise_error(mock_requests_get, lastfm_client):

    mock_requests_get
    with pytest.raises(ValueError):
        lastfm_client.fetch_info_data(type="playlist")

def test_fetch_info_data_invalid_kwarg_raise_error(mock_requests_get, lastfm_client):
    mock_requests_get
    with pytest.raises(ValueError):
        lastfm_client.fetch_info_data(type="artist", unknown_kwarg= "oops")

def test_fetch_top_tags_invalid_type_raise_error(mock_requests_get, lastfm_client):
    mock_requests_get
    with pytest.raises(ValueError):
         lastfm_client.fetch_top_tags(type="playlist")

def test_fetch_top_tags_invalid_kwargs_raise_error(mock_requests_get, lastfm_client):
    mock_requests_get
    with pytest.raises(ValueError):
        lastfm_client.fetch_top_tags(type="artist", unknown_kwarg="oops")


