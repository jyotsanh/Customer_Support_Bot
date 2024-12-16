from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Ensure the database directory exists
DATABASE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
os.makedirs(DATABASE_DIR, exist_ok=True)

# SQLite database path
DATABASE_PATH = os.path.join(DATABASE_DIR, 'hotel.sqlite')

# Create SQLAlchemy engine
engine = create_engine(f'sqlite:///{DATABASE_PATH}', 
                       connect_args={'check_same_thread': False})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

def get_db():
    """
    Dependency that creates a new database session for each request.
    Yields the session and ensures it's closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
if __name__ == "__main__":
    db = get_db()