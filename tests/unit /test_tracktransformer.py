import pytest 
from tests.mock_api_responses import Mocklastfmresponses

def test_transform_recent_tracks_output(track_transformer):
    mock_recent_tracks_response = Mocklastfmresponses.mock_recent_tracks_response()
    simulate_extracted_response = mock_recent_tracks_response["recenttracks"]["track"]
    result_transformed = track_transformer.transform_recent_tracks(tracks_json=simulate_extracted_response)
    assert isinstance(result_transformed, list)
    assert all(isinstance(result, dict) for result in result_transformed)

def test_transform_album_info_output(track_transformer):
    mock_album_info_response = Mocklastfmresponses.mock_album_info_response()
    simulate_extracted_response = mock_album_info_response['album']
    result_transformed = track_transformer.transform_info(data=simulate_extracted_response, entity='album')
    assert isinstance(result_transformed, dict)

def test_transform_track_info_output(track_transformer):
    mock_track_info_response = Mocklastfmresponses.mock_track_info_response()
    simulate_extracted_response = mock_track_info_response['track']
    result_transformed = track_transformer.transform_info(data=simulate_extracted_response, entity='track')
    assert isinstance(result_transformed, dict)

def test_transform_info_raiseError(track_transformer): 
    with pytest.raises(ValueError):
        mock_track_info_response = Mocklastfmresponses.mock_track_info_response()
        simulate_extracted_response = mock_track_info_response['track']
        track_transformer.transform_info(data=simulate_extracted_response, entity='artist')
        
def test_build_music_genre_list_output(track_transformer):
    mock_tag_response = Mocklastfmresponses.mock_album_tag_response()
    simulate_extracted_response = [tag["name"] for tag in mock_tag_response["toptags"]["tag"]]
    result_transformed = track_transformer.build_music_genre_list(extracted_tags=simulate_extracted_response)
    assert isinstance(result_transformed, list)
    assert all(isinstance(result, str) for result in result_transformed)


