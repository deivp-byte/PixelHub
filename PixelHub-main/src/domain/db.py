from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session   
from .config import DB_URL


class Base(DeclarativeBase):
    pass

engine = create_engine(
    DB_URL
)