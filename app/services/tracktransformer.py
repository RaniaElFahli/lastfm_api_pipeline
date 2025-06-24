import pandas as pd 
import logging

class TrackTransformer:
    
    def __init__(self, genre_csv_path):
        self.list_genres = self._load_genres_list(genre_csv_path)
    
    def _load_genres_list(self, path):
        df = pd.read_csv(path)
        return list(df['sub_genre'].str.lower())

    def transform_recent_tracks(self, tracks_json:list[dict]) -> list[dict]:
        df = pd.json_normalize(tracks_json)
    
        df = df.rename(columns={
        "name": "track_name",
        "artist.#text": "artist",
        "album.#text": "album",
        "date.uts": "timestamp"
    })
        df = df[["track_name", "artist", "album", "timestamp"]]
        df = df.dropna(subset=["timestamp"])


        df["timestamp"] = df["timestamp"].astype(int)
        df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")

        return df.to_dict(orient="records")
    
    def transform_info(self, data: dict, entity: str) -> dict:
        
        if entity == "track": 
            return {
                "title": data.get("name"),
                "duration": int(data.get("duration", 0)) if data.get("duration") else None,
            }

        elif entity == "album":
            return  {
                    "album_title": data.get("name"),
                    "image_url": data.get("image", [])[-1].get("#text") if data.get("image") else None,
                    "release_date": data.get("wiki", {}).get("published") if data.get("wiki") else None
            }
        else:
            raise ValueError(f"Unknown entity type: {entity}")
        
        
    def build_music_genre_list(self, extracted_tags: list[str]): 
        return [tag for tag in extracted_tags if tag in self.list_genres]

