import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic import command

# Load environment variables
load_dotenv()

# Get database url with dotenv
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test_db.db")

# Define engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
