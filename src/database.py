from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = os.environ.get('GLAUCOMA_API_DB_CONNECTION', None)
# "postgresql://user:password@postgresserver/db"

engine = create_engine(
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    SQLALCHEMY_DATABASE_URL
)
# Session Local
# Each instance of the SessionLocal class will be a database session. The class itself is not a database session yet.
# But once we create an instance of the SessionLocal class, this instance will be the actual database session.
# We name it SessionLocal to distinguish it from the Session we are importing from SQLAlchemy
# SessionLocal = sessionmaker(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# We inherit this class at each of the database models or classes (the ORM models):
Base = declarative_base()
