import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

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

def store_liquidation_data(liquidation_data):
    # Create a new session
    session = Session()

    received_timestamp = datetime.utcnow()
    event_time = datetime.fromtimestamp(liquidation_data["E"]/1000)
    # Create a new Liquidation object
    new_liquidation = Liquidation(
        event_type=liquidation_data["e"],
        event_time=event_time,
        symbol=liquidation_data["o"]["s"],
        side=liquidation_data["o"]["S"],
        order_type=liquidation_data["o"]["o"],
        time_in_force=liquidation_data["o"]["f"],
        quantity=liquidation_data["o"]["q"],
        price=liquidation_data["o"]["p"],
        average_price=liquidation_data["o"]["ap"],
        order_status=liquidation_data["o"]["X"],
        last_filled_quantity=liquidation_data["o"]["l"],
        filled_accumulated_quantity=liquidation_data["o"]["z"],
        order_trade_time=datetime.fromtimestamp(liquidation_data["o"]["T"]/1000),
        received_timestamp=received_timestamp,

    )
    # Add the new Liquidation object to the session
    session.add(new_liquidation)
    # Commit the transaction
    session.commit()
    # Close the session
    session.close()