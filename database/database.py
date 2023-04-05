import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Import the Base class and the required ORM models from models.py
from .models import Base, Liquidation

# Read the database configuration from environment variables
DB_USER = os.environ["POSTGRES_USER"]
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DB_PORT = os.environ["POSTGRES_PORT"]
DB_NAME = os.environ["POSTGRES_DB"]

# Create a connection URL using the configuration values
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@db:{DB_PORT}/{DB_NAME}"

# Create a database engine
engine = create_engine(DATABASE_URL)

# Create a session factory
Session = sessionmaker(bind=engine)

# Create tables if they don't exist
Base.metadata.create_all(engine)