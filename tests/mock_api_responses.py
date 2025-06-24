#### Mocks of Lastfm responses for the different unit tests. 

class Mocklastfmresponses:

   @staticmethod 
   def mock_recent_tracks_response():
    return {
        "recenttracks": {
            "track": [
                {
                    "name": "Weird Fishes / Arpeggi",
                    "artist": {"#text": "Radiohead"},
                    "album": {"#text": "In Rainbows"},
                    "date": {"uts": "1749296024"}
                }, 
            {
                    "name": "Liquid Fire",
                    "artist": {"#text": "Gojira"},
                    "album": {"#text": "L'Enfant Sauvage"},
                    "date": {"uts": "1749896024"}
                }

            ]
        }
    }

   
   @staticmethod
   def mock_album_info_response():
      return {
    "album": {
    "artist": "Radiohead",
    "name" : "In Rainbows",
    "mbid": "1475431a-cfd3-43ad-bf09-b3826118446f",
    "tags": {
      "tag": [
        {
          "url": "https://www.last.fm/tag/alternative",
          "name": "alternative"
        },
        {
          "url": "https://www.last.fm/tag/alternative+rock",
          "name": "alternative rock"
        },
        {
          "url": "https://www.last.fm/tag/2007",
          "name": "2007"
        },
        {
          "url": "https://www.last.fm/tag/rock",
          "name": "rock"
        },
        {
          "url": "https://www.last.fm/tag/indie",
          "name": "indie"
        }
      ]
    },
    "playcount": "183233257",
    "image": [
      {
        "size": "small",
        "#text": "https://lastfm.freetls.fastly.net/i/u/34s/9dbcd9399ac3e622b4f508323155b644.jpg"
      },
      {
        "size": "medium",
        "#text": "https://lastfm.freetls.fastly.net/i/u/64s/9dbcd9399ac3e622b4f508323155b644.jpg"
      },
      {
        "size": "large",
        "#text": "https://lastfm.freetls.fastly.net/i/u/174s/9dbcd9399ac3e622b4f508323155b644.jpg"
      },
      {
        "size": "extralarge",
        "#text": "https://lastfm.freetls.fastly.net/i/u/300x300/9dbcd9399ac3e622b4f508323155b644.jpg"
      },
      {
        "size": "mega",
        "#text": "https://lastfm.freetls.fastly.net/i/u/300x300/9dbcd9399ac3e622b4f508323155b644.jpg"
      },
      {
        "size": "",
        "#text": "https://lastfm.freetls.fastly.net/i/u/300x300/9dbcd9399ac3e622b4f508323155b644.jpg"
      }]}}

   
   @staticmethod
   def mock_track_info_response():
      return {
    "track": {
        "name": "Weird Fishes / Arpeggi",
        "mbid": "9f317135-f788-4511-96e8-d00161b4ad6a",
        "url": "https://www.last.fm/music/Radiohead/_/Let+Down",
        "duration": "337000",
        "streamable": {
        "#text": "0",
        "fulltrack": "0"
        },
        "listeners": "1778419",
        "playcount": "22128753",
        "artist": {
        "name": "Radiohead",
        "mbid": "a74b1b7f-71a5-4011-9441-d0b5e4122711",
        "url": "https://www.last.fm/music/Radiohead"
        }}}
   
   @staticmethod
   def mock_artist_tag_response():
      return {"toptags": {
    "tag": [
      {
        "count": 81,
        "name": "alternative rock",
        "url": "https://www.last.fm/tag/alternative+rock"
      },
      {
        "count": 73,
        "name": "rock",
        "url": "https://www.last.fm/tag/rock"
      },
      {
        "count": 59,
        "name": "indie",
        "url": "https://www.last.fm/tag/indie"
      }]}}
   
   @staticmethod
   def mock_album_tag_response():
      return{"toptags": {
    "tag": [
      {
        "count": 100,
        "name": "albums I own",
        "url": "https://www.last.fm/tag/albums+I+own"
      },
      {
        "count": 69,
        "name": "alternative",
        "url": "https://www.last.fm/tag/alternative"
      },
      {
        "count": 67,
        "name": "alternative rock",
        "url": "https://www.last.fm/tag/alternative+rock"
      },
      {
        "count": 53,
        "name": "2007",
        "url": "https://www.last.fm/tag/2007"
      }]}}
