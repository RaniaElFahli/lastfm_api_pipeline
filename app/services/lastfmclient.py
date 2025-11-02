import requests 
import logging
from prefect_deployment.prefect_flow import make_loader


class LASTFMClient:
    def __init__(self, api_key: str, base_url : str, username: str, logger):
        self.api_key = api_key
        self.base_url = base_url
        self.username = username 
        self.logger = logger

    def  call_lastfm_client(self, url, params:dict) -> dict:
        try:
            r = requests.get(url,timeout=10, params=params)
            r.raise_for_status()
            return r.json()
        
        except requests.exceptions.RequestException as err:
            print (err)
            raise  
    
    def check_call_lastfm_client_code(self, url, params): 
        try:
            r = requests.get(url, params=params, timeout=10)
            r.raise_for_status()
            return r.status_code 
        except requests.exceptions.Timeout as errt:
            print (errt)
            raise
        except requests.exceptions.HTTPError as errh:
            print (errh)
            raise
        except requests.exceptions.ConnectionError as errc:
            print (errc)
            raise

    def fetch_recent_tracks(self) -> list[dict]:
        
        all_tracks = []
        page = 1
        per_page = 200
        logger = self.logger
        loader = make_loader(logger)
        last_timestamp = loader._get_last_timestamp()
        
        while not stop: 
            params = {
            "method" : "user.getRecentTracks", 
            "user" : self.username, 
            "api_key" : self.api_key, 
            "format" : "json",
            "limit": per_page
        }
            call_tracks = self.call_lastfm_client(url=self.base_url, params=params)
            tracks = call_tracks.get("recenttracks", {}).get("track", [])
            self.logger.info(f'"Returned status code {self.check_call_lastfm_client_code(url=self.base_url, params=params)}"')
            
            if not tracks:
                break

        for track in tracks:
            ts = track.get("date", {}).get("uts")
            ts = int(ts) 
            if last_timestamp and ts and ts <= last_timestamp:
                stop = True
                break
            all_tracks.append(track)

        self.logger.info(f"Fetched page {page} = total {len(all_tracks)} tracks")

        page += 1
        return all_tracks

    def fetch_info_data(self, type:str, **kwargs) -> dict:
    
        if type not in ['track', 'album']:
            raise ValueError(f"Type {type} not supported !")
        
        allowed_kwargs = {"artist", "album", "track"}
        for k in kwargs:
            if k not in allowed_kwargs:
                raise ValueError(f"Invalid kwarg: {k}")
        
        method_map = { 
        "track" : "track.getInfo", 
        "album" : "album.getInfo", 
    }

        params= {
        "method" : method_map[type], 
        "api_key": self.api_key, 
        "format" : "json",
        "autocorrect": 1,
        **kwargs
    }
        data = self.call_lastfm_client(url=self.base_url, params=params)
        self.logger.info(f'"Returned status code {self.check_call_lastfm_client_code(url=self.base_url, params=params)}"')
        return data.get(type, {}) 
    
    def fetch_top_tags(self, type:str, **kwargs):

        if type not in ['artist', 'album']:
            raise ValueError(f"Type {type} not supported !")
        
        allowed_kwargs = {"artist", "album"}
        for k in kwargs:
            if k not in allowed_kwargs:
                raise ValueError(f"Invalid kwarg: {k}")

        method_map = {
            "artist" : "artist.getTopTags", 
            "album" : "album.getTopTags"
        }

        params = {
        "method" : method_map[type], 
        "api_key": self.api_key, 
        "format" : "json",
        "autocorrect": 1,
        **kwargs
        }
        data = self.call_lastfm_client(url=self.base_url, params=params)
        self.logger.info(f'"Returned status code {self.check_call_lastfm_client_code(url=self.base_url, params=params)}"')
        tags_data = data.get("toptags", {}).get("tag", [])
        if isinstance(tags_data, dict):
            tags_data = [tags_data]
        extracted_tags = [tag.get("name") for tag in tags_data if isinstance(tag, dict)]
        return extracted_tags
