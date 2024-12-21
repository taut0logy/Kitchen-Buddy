from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URI

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)


def get_session():
    return Session()
