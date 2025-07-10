from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "http://ws.audioscrobbler.com/2.0/"
USERNAME = os.getenv("username")
DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

PREFECT_LOGGING_EXTRA_LOGGERS = [
    "lastfm_pipeline.lastfmclient",
    "lastfm_pipeline.trackloader"
]

os.environ["PREFECT_LOGGING_EXTRA_LOGGERS"] = ",".join(PREFECT_LOGGING_EXTRA_LOGGERS)

API_BASE_URL = "http://127.0.0.1:8000/"