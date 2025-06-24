# lastfm_api_pipeline
An example of a complete ETL pipeline using Lastfm API's user data :

This project is a full ETL pipeline that extracts data from the Last.fm API, processes it, and stores it in a PostgreSQL database. It is designed as a portfolio project showcasing
different skills : API consumption, data transformation, data modeling, testing and simple orchestration. 

Features of this pipeline :

Fetch recent listening history for a Last.fm user.

Request detailed metadata for tracks, albums, and artists recently listened to.

Normalize and clean data.

Insert data into a PostgreSQL database with proper relationships into a star model.

Handle deduplication and integrity checks.

Logging and orchestration with Prefect.

Fully tested pipeline (unit + integration tests with pytest).

Tech Stack : 

Python 3.12

PostgreSQL

SQLAlchemy ORM

Prefect

Pytest

Poetry 