from sqlalchemy.orm import Session
from sqlalchemy import create_engine 
from app.config import DATABASE_URL
from app.models import Base


engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

session = Session(engine)