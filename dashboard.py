import streamlit as st
import requests 
import pandas as pd
import plotly.express as px
from app.config import API_BASE_URL, USERNAME

st.set_page_config(page_title="Music Dashboard", layout="wide")

@st.cache_data(ttl=3600)
def fetch_top_artists(limit=5):
    response = requests.get(f"{API_BASE_URL}/top-artists?limit={limit}")
    return response.json()

@st.cache_data(ttl=3600)
def fetch_top_tracks(limit=5):
    response = requests.get(f"{API_BASE_URL}/top-tracks?limit={limit}")
    return response.json()

@st.cache_data(ttl=3600)
def fetch_top_genres(limit=5):
    response = requests.get(f"{API_BASE_URL}/top-genres?limit={limit}")
    return response.json()

@st.cache_data(ttl=3600)
def fetch_genre_diversity():
    response = requests.get(f"{API_BASE_URL}/genre-diversity")
    return response.json()

@st.cache_data(ttl=3600)
def fetch_daily_listens():
    response = requests.get(f"{API_BASE_URL}/daily-listens")
    return response.json()

st.title(f"{USERNAME}'s personal music dashboard")

st.markdown("""
This dashboard provides insights into your music listening habits, including top artists, tracks, genres, and daily listening duration.
""")

col1, col2 = st.columns(2)

with col1:
    st.header(f"{USERNAME}'s Top Artists")
    artists = fetch_top_artists(10)
    df_artists = pd.DataFrame(artists)
    fig = px.bar(df_artists, x='artist_name', y='listen_count', 
                 labels={'artist_name': 'Artist', 'listen_count': 'Number of Listens'})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header(f"{USERNAME}'s Top Genres")
    genres = fetch_top_genres(10)
    df_genres = pd.DataFrame(genres)
    fig = px.pie(df_genres, names='genre_name', values='listen_count',
                 title="Genre Distribution")
    st.plotly_chart(fig, use_container_width=True)

st.header(f"{USERNAME}'s Daily Listening History")
daily_data = fetch_daily_listens()
if daily_data:
    df_daily = pd.DataFrame(daily_data)
    df_daily['date_time'] = pd.to_datetime(df_daily['date_time'])
    df_daily = df_daily.sort_values('date_time')
    
    fig = px.line(df_daily, x='date_time', y='duration_count',
                  labels={'date_time': 'Date', 'duration_count': 'Minutes Listened'})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for daily listening history")

st.header(f"{USERNAME}'s Top Tracks")
tracks = fetch_top_tracks(10)
df_tracks = pd.DataFrame(tracks)
st.dataframe(df_tracks[['track_name', 'artist_name', 'listen_count']]
             .rename(columns={
                 'track_name': 'Title',
                 'artist_name': 'Artist',
                 'listen_count': 'Number of Listens'
             }), hide_index=True, use_container_width=True)