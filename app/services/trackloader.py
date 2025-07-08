from app.models import Artists, Tracks, AlbumGenre, Albums, MusicGenre, ArtistGenre, RecentTracks
from sqlalchemy.orm import Session
import logging
from app.decorators import commit_or_rollback


logger = logging.getLogger(name="lastfm_pipeline.trackloader")

class TrackLoader:

    def __init__(self, db: Session, extractor, transformer):
        self.db = db
        self.extractor = extractor
        self.transformer = transformer 

    def _get_or_create_artist(self, artist_name:str) -> int:
        artist = self.db.query(Artists).filter_by(artist_name=artist_name).first()

        if artist:
            return artist.artist_id
        
        else:
            new_artist = Artists(artist_name=artist_name)
            self.db.add(new_artist)
            self.db.flush()
            logger.info(f'{artist_name} : new artist inserted in Artists table')
            return new_artist.artist_id
        
    def _get_or_create_album(self, album_title:str, artist_name:str, artist_id:int)->int:
        album = self.db.query(Albums).filter_by(album_title=album_title).first()
        
        if album: 
            return album.album_id
        
        else: 
            album_info = self.extractor.fetch_info_data("album", artist=artist_name, album=album_title)
            album_data = self.transformer.transform_info(album_info, entity="album")
            artist_id = artist_id
            new_album = Albums(
                album_title=album_title, 
                release_date= album_data['release_date'], 
                image_url=album_data['image_url'], 
                artist_id=artist_id )
            self.db.add(new_album)
            self.db.flush()
            logger.info(f'{album_title} : new album inserted in Albums table')
            return new_album.album_id
        
    def _get_or_create_track(self, track_name:str, artist_name:str, album_title:str):
        track = self.db.query(Tracks).filter_by(track_title=track_name).first()
        
        if track:
            return track.track_id, track.artist_id, track.album_id     
        else: 
            track_info = self.extractor.fetch_info_data("track", artist=artist_name, track=track_name)
            track_data = self.transformer.transform_info(track_info, entity="track")
            artist_id = self._get_or_create_artist(artist_name=artist_name)
            album_id = self._get_or_create_album(album_title=album_title, artist_name=artist_name, artist_id=artist_id)
            new_track = Tracks(
                track_title = track_name, 
                duration=track_data['duration'], 
                artist_id = artist_id, 
                album_id = album_id
            )
            self.db.add(new_track)
            self.db.flush()
            logger.info(f'{track_name} : new track inserted in Tracks table')
            return new_track.track_id, new_track.artist_id, new_track.album_id

    @commit_or_rollback
    def load_recent_tracks(self, tracks_data: list[dict]):
        for track in tracks_data:
            track_id, artist_id, album_id = self._get_or_create_track(track_name=track['track_name'], artist_name=track['artist'], album_title=track['album'])
            existing_track = self.db.query(RecentTracks).filter_by(timestamp=track['timestamp'], track_id=track_id).first()
            if existing_track:
                logger.info(f'RecentTracks duplicate ignored for {existing_track}')
            else: 
                new_recent_track = RecentTracks(
                    timestamp = track['timestamp'], 
                    date_time= track['datetime'], 
                    track_id = track_id, 
                    album_id = album_id, 
                    artist_id = artist_id
                )
                self.db.add(new_recent_track)
                logger.info(f'{len(tracks_data)} listenings inserted into RecentTracks table.')

    def _get_or_create_music_genre(self, genre_name:str) ->int:
        genre = self.db.query(MusicGenre).filter_by(genre_name=genre_name).first()

        if genre: 
            return genre.genre_id
        
        else:
            new_genre = MusicGenre(genre_name=genre_name)
            self.db.add(new_genre)
            self.db.flush()
            logger.info(f'New genre inserted into MusicGenre table : {genre_name}')
            return new_genre.genre_id

    @commit_or_rollback
    def load_artist_genres(self, artist_name:str):
        artist_id = self._get_or_create_artist(artist_name=artist_name)
        extracted_artist_tags = self.extractor.fetch_top_tags(type="artist", artist=artist_name)
        genre_names = self.transformer.build_music_genre_list(extracted_tags=extracted_artist_tags)
        for genre_name in genre_names:
            genre_id = self._get_or_create_music_genre(genre_name=genre_name)
            artist_genre = self.db.query(ArtistGenre).filter_by(genre_id=genre_id, artist_id=artist_id).first()
            if artist_genre:
                logger.info(f'ArtistGenre duplicate ignored : {genre_name} already existing for {artist_name}')

            else: 
                new_artist_genre = ArtistGenre(artist_id=artist_id, genre_id=genre_id)
                self.db.add(new_artist_genre)
                logger.info(f'{genre_name} inserted for {artist_name} in ArtistGenre table')

    @commit_or_rollback
    def load_album_genres(self, album_title:str, artist_name:str):
        artist_id = self._get_or_create_artist(artist_name=artist_name)
        album_id = self._get_or_create_album(album_title=album_title, artist_name=artist_name, artist_id=artist_id)
        extracted_album_tags = self.extractor.fetch_top_tags(type="album", artist=artist_name, album=album_title)
        genre_names = self.transformer.build_music_genre_list(extracted_tags=extracted_album_tags)
        for genre_name in genre_names:
            genre_id = self._get_or_create_music_genre(genre_name=genre_name)
            album_genre = self.db.query(AlbumGenre).filter_by(genre_id=genre_id, album_id=album_id).first()
            if album_genre: 
                logger.info(f'AlbumGenre duplicate ignored : {genre_name} already existing for {album_title}')
            else:
                new_album_genre = AlbumGenre(genre_id=genre_id, album_id=album_id)
                self.db.add(new_album_genre)
                logger.info(f'{genre_name} inserted for {album_title} in AlbumGenre table')


