def load_orm(**kwargs):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    from datetime import datetime
    from app.models import Base, MusicGenre, Artists, ArtistGenre, Albums, AlbumGenre, Tracks, RecentTracks

    url = f"postgresql+psycopg2://{kwargs['user']}:@{kwargs['host']}:{kwargs['port']}/{kwargs['dbname']}"
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    session = Session(engine)

    # 1. Genres
    genres_dict = {}
    genre_names = ['Alternative Rock', 'Ambient', 'Indie Rock', 'Progressive Rock', 'Avant-Garde']
    for name in genre_names:
        g = MusicGenre(genre_name=name)
        session.add(g)
        genres_dict[name] = g
    session.commit()

    # 2. Artists
    artists_dict = {}
    artist_names = ['Radiohead', 'Placebo', 'Massive Attack', 'Tame Impala', 'Portishead', 'The Strokes', 'Arctic Monkeys']
    for name in artist_names:
        a = Artists(artist_name=name)
        session.add(a)
        artists_dict[name] = a
    session.commit()

    # 3. Artist Genres
    artist_genre_mappings = [
        ('Radiohead', 'Alternative Rock'),
        ('Radiohead', 'Avant-Garde'),
        ('Placebo', 'Alternative Rock'),
        ('Massive Attack', 'Ambient'),
        ('Massive Attack', 'Avant-Garde'),
        ('Tame Impala', 'Indie Rock'),
        ('Portishead', 'Ambient'),
        ('Portishead', 'Avant-Garde'),
        ('The Strokes', 'Alternative Rock'),
        ('Arctic Monkeys', 'Alternative Rock'),
        ('Arctic Monkeys', 'Indie Rock'),
    ]

    for artist_name, genre_name in artist_genre_mappings:
        ag = ArtistGenre(
            artist_id=artists_dict[artist_name].artist_id,
            genre_id=genres_dict[genre_name].genre_id
        )
        session.add(ag)
    session.commit()

    # 4. Albums
    albums_info = [
        ('OK Computer', '1997-06-16', 'https://example.com/radiohead_ok.jpg', 'Radiohead'),
        ('Meds', '2006-03-13', 'https://example.com/placebo_meds.jpg', 'Placebo'),
        ('Mezzanine', '1998-04-20', 'https://example.com/massiveattack_mez.jpg', 'Massive Attack'),
        ('Currents', '2015-07-17', 'https://example.com/tameimpala_currents.jpg', 'Tame Impala'),
        ('Dummy', '1994-08-22', 'https://example.com/portishead_dummy.jpg', 'Portishead'),
        ('Is This It', '2001-07-30', 'https://example.com/strokes_isthisit.jpg', 'The Strokes'),
        ('AM', '2013-09-09', 'https://example.com/am.jpg', 'Arctic Monkeys'),
    ]

    albums_dict = {}
    for title, date_str, img_url, artist_name in albums_info:
        album = Albums(
            album_title=title,
            release_date=datetime.strptime(date_str, '%Y-%m-%d').date(),
            image_url=img_url,
            artist_id=artists_dict[artist_name].artist_id
        )
        session.add(album)
        albums_dict[title] = album
    session.commit()

    # 5. Album Genres
    album_genre_mappings = [
        ('OK Computer', 'Alternative Rock'),
        ('OK Computer', 'Avant-Garde'),
        ('Meds', 'Alternative Rock'),
        ('Mezzanine', 'Ambient'),
        ('Mezzanine', 'Avant-Garde'),
        ('Currents', 'Indie Rock'),
        ('Dummy', 'Ambient'),
        ('Dummy', 'Avant-Garde'),
        ('Is This It', 'Alternative Rock'),
        ('AM', 'Alternative Rock'),
        ('AM', 'Indie Rock'),
    ]

    for album_title, genre_name in album_genre_mappings:
        ag = AlbumGenre(
            album_id=albums_dict[album_title].album_id,
            genre_id=genres_dict[genre_name].genre_id
        )
        session.add(ag)
    session.commit()

    # 6. Tracks
    tracks_info = [
        ('Paranoid Android', 387, 'OK Computer', 'Radiohead'),
        ('The Bitter End', 231, 'Meds', 'Placebo'),
        ('Teardrop', 311, 'Mezzanine', 'Massive Attack'),
        ('Let It Happen', 463, 'Currents', 'Tame Impala'),
        ('Glory Box', 300, 'Dummy', 'Portishead'),
        ('Last Nite', 230, 'Is This It', 'The Strokes'),
        ('Do I Wanna Know?', 272, 'AM', 'Arctic Monkeys'),
    ]

    tracks_dict = {}
    for title, duration, album_title, artist_name in tracks_info:
        track = Tracks(
            track_title=title,
            duration=duration,
            album_id=albums_dict[album_title].album_id,
            artist_id=artists_dict[artist_name].artist_id
        )
        session.add(track)
        tracks_dict[title] = track
    session.commit()

    # 7. Recent Tracks
    recent_tracks_info = [
        (1718700000000, '2024-06-18 09:00:00', 'Paranoid Android', 'OK Computer', 'Radiohead'),
        (1718700600000, '2024-06-18 09:10:00', 'The Bitter End', 'Meds', 'Placebo'),
        (1718701200000, '2024-06-18 09:20:00', 'Teardrop', 'Mezzanine', 'Massive Attack'),
        (1718701800000, '2024-06-18 09:30:00', 'Glory Box', 'Dummy', 'Portishead'),
        (1718702400000, '2024-06-18 09:40:00', 'Do I Wanna Know?', 'AM', 'Arctic Monkeys'),
    ]

    for timestamp, date_time_str, track_title, album_title, artist_name in recent_tracks_info:
        rt = RecentTracks(
            timestamp=timestamp,
            date_time=date_time_str,
            track_id=tracks_dict[track_title].track_id,
            album_id=albums_dict[album_title].album_id,
            artist_id=artists_dict[artist_name].artist_id
        )
        session.add(rt)
    session.commit()

    session.close()