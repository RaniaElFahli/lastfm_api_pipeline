from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, TIMESTAMP, TEXT, ForeignKey, BIGINT, PrimaryKeyConstraint, UniqueConstraint
from datetime import datetime
from typing import List

metadata_obj = MetaData()

class Base(DeclarativeBase):
    pass

class Artists(Base):
    __tablename__ = "artists"

    artist_id: Mapped[int] = mapped_column(primary_key=True)
    artist_name: Mapped[str] = mapped_column(String(30))

    tracks: Mapped[List["Tracks"]] = relationship(back_populates="artist")
    albums: Mapped[List["Albums"]] = relationship(back_populates="artist")
    artist_genres: Mapped[List["ArtistGenre"]] = relationship(back_populates="artist")

    def __repr__(self) -> str:
        return f"artists(artist_id={self.artist_id!r}, artist_name={self.artist_name!r})"
    
class Albums(Base): 
    __tablename__ = "albums"
    __table_args__ = (UniqueConstraint(
        "album_id", "artist_id", name="unique_album_artist_constraint"),
        {}
      
    )

    album_id: Mapped[int] = mapped_column(primary_key=True)
    album_title: Mapped[str] = mapped_column(String(100))
    release_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    image_url: Mapped[str] = mapped_column(TEXT, nullable=True)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.artist_id")) 

    artist: Mapped["Artists"] = relationship(back_populates="albums")
    tracks: Mapped[List["Tracks"]] = relationship(back_populates="album")
    album_genres: Mapped[List["AlbumGenre"]] = relationship(back_populates="album")

    def __repr__(self) -> str:
        return f"albums(album_id={self.album_id!r}, album_title={self.album_title!r}, release_date={self.release_date!r}, image_url={self.image_url!r}, artist_id={self.artist_id!r})"

class Tracks(Base): 
    __tablename__ = "tracks"
    __table_args__ = (UniqueConstraint(
        "album_id", "artist_id", "track_id", name="unique_album_artist_track_constraint"),
        {}    
    )


    track_id: Mapped[int] = mapped_column(primary_key=True)
    track_title: Mapped[str] = mapped_column(String(100), nullable=False)
    duration: Mapped[int]
    album_id: Mapped[int] = mapped_column(ForeignKey("albums.album_id"))
    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.artist_id"))

    album: Mapped["Albums"] = relationship(back_populates="tracks")
    artist: Mapped["Artists"] = relationship(back_populates="tracks")

    def __repr__(self) -> str:
        return f"tracks(track_id={self.track_id!r}, track_title={self.track_title!r}, duration={self.duration!r}, album_id={self.album_id!r})"


class RecentTracks(Base): 
    __tablename__ = "recent_tracks"
    __table_args__ = (
         PrimaryKeyConstraint("listen_id", "timestamp", name="recent_tracks_pk"), 
         UniqueConstraint(
        "album_id", "artist_id", "track_id", "listen_id", "timestamp", name="unique_recent_track_constraint") 
    )


    listen_id: Mapped[int] = mapped_column(nullable=False, autoincrement=True)
    timestamp: Mapped[int] = mapped_column(BIGINT, nullable=False)
    date_time: Mapped[datetime] = mapped_column(TIMESTAMP)
    track_id: Mapped[int] = mapped_column(ForeignKey("tracks.track_id"))
    album_id: Mapped[int] = mapped_column(ForeignKey("albums.album_id"))
    artist_id:Mapped[int] = mapped_column(ForeignKey("artists.artist_id"))

    def __repr__(self) -> str:
        return f"recent_tracks(listen_id={self.listen_id!r},timestamp={self.timestamp!r}, date_time={self.date_time!r}, track_id={self.track_id!r}, album_id={self.album_id!r}, artist_id={self.artist_id!r})"
    

class MusicGenre(Base): 
    __tablename__ = "music_genre"

    genre_id: Mapped[int] = mapped_column(primary_key=True)
    genre_name: Mapped[str] = mapped_column(String(100), nullable=False)

    artist_genres: Mapped[List["ArtistGenre"]] = relationship(back_populates="genre")
    album_genres: Mapped[List["AlbumGenre"]] = relationship(back_populates="genre")


    def __repr__(self) -> str:
        return f"music_genre(genre_id={self.genre_id!r}, genre_name{self.genre_name!r})"


class ArtistGenre(Base):
    __tablename__ = "artist_genres"
    __table_args__ = (
         PrimaryKeyConstraint("artist_id", "genre_id", name="artist_genres_pk"), 
         {}
    )

    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.artist_id"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("music_genre.genre_id"))

    
    genre: Mapped["MusicGenre"] = relationship(back_populates="artist_genres")
    artist: Mapped["Artists"] = relationship(back_populates="artist_genres")

    def __repr__(self)-> str:
        return f"artist_genres(artist_id={self.artist_id!r}, genre_id={self.genre_id!r})"

class AlbumGenre(Base): 
    __tablename__ = "album_genres"
    __table_args__ = (
         PrimaryKeyConstraint("album_id", "genre_id", name="album_genres_pk"), 
         {}
    )


    album_id: Mapped[int] = mapped_column(ForeignKey("albums.album_id"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("music_genre.genre_id"))
    album: Mapped["Albums"] = relationship(back_populates="album_genres")
    genre: Mapped["MusicGenre"] = relationship(back_populates="album_genres")

    def __repr__(self)-> str:
        return f"album_genres(album_id={self.album_id!r}, genre_id={self.genre_id!r})"
