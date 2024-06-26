from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from configuration.settings import settings
# import pymysql

DB_USER = settings.SINGLE_STORE_USER
DB_PASSWORD = settings.SINGLE_STORE_PASSWORD
DB_HOST = settings.SINGLE_STORE_HOST
DB_PORT = settings.SINGLE_STORE_PORT
DB_DATABASE = settings.SINGLE_STORE_DB
DB_CA = settings.SINGLE_STORE_CA

ssl_args = {
    "ssl": {
        "ca": DB_CA
    }
}


def get_engine():
    url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    engine = create_engine(url, pool_size=50, echo=False, connect_args=ssl_args)
    return engine


def get_session() -> Session:
    engine = get_engine()
    session = sessionmaker(bind=engine)
    return session()


db = get_session()
