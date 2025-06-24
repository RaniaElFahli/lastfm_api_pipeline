class LastfmPipeline:
    def __init__(self, extractor, transformer, loader):
        self.extractor = extractor
        self.transformer = transformer     
        self.loader = loader
    
    def run(self):
     tracks_json = self.extractor.fetch_recent_tracks()
     tracks_data = self.transformer.transform_recent_tracks(tracks_json=tracks_json)
     self.loader.load_recent_tracks(tracks_data=tracks_data)
     for track in tracks_data: 
          artist = track['artist']
          album = track['album']
          self.loader.load_artist_genres(artist_name=artist)
          self.loader.load_album_genres(artist_name=artist, album_title=album)