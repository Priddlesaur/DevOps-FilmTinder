import os

from alembic.config import Config
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

# Run migrations
alembic_cfg = Config("alembic.ini")
alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)
command.upgrade(alembic_cfg, "head")

# Function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
