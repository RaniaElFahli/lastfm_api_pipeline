from sqlalchemy import create_engine
from app.config import DATABASE_URL
import pandas as pd 

engine = create_engine(DATABASE_URL)


def get_top_artists(limit=10):
    query = """
        select artist, count(*) as listen_count
        from recent_tracks
        group by artist
        order by listen_count desc
        limit ?
    """
    return pd.read_sql_query(query, engine, params=(limit,))
    
def get_top_tracks(limit=10):
    query = """
        select track_name, artist, count(*) as listen_count
        from recent_tracks
        group by track_name, artist
        order by listen_count desc
        limit ? 
    """
    return pd.read_sql_query(query, engine, params=(limit,))
    
def get_listens_per_day():
    query = """
    select DATE(datetime) AS day, count(*) as listen_count
    from recent_tracks
    group by day 
    order by day desc
"""
    return pd.read_sql_query(query, engine)
