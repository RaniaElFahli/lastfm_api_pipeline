import requests 

class LASTFMClient:
    def __init__(self, api_key: str, base_url : str, username: str, fetch_limit:int, logger):
        self.api_key = api_key
        self.base_url = base_url
        self.username = username 
        self.fetch_limit = fetch_limit
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
        params = {
        "method" : "user.getRecentTracks", 
        "user" : self.username, 
        "api_key" : self.api_key, 
        "format" : "json",
        "limit": self.fetch_limit
    }
        data = self.call_lastfm_client(url=self.base_url, params=params)
        self.logger.info(f'"Returned status code {self.check_call_lastfm_client_code(url=self.base_url, params=params)}"')
        self.logger.info(f'Fetched {self.fetch_limit} recent tracks for user : {self.username}')
        return data.get("recenttracks", {}).get("track", [])
    
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
