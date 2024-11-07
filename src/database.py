import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Get database url with dotenv
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test_db.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
