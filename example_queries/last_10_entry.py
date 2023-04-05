import sys
from pathlib import Path

app_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(app_dir))

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from database.models import Liquidation
from sqlalchemy.orm import sessionmaker
import pandas as pd
from datetime import datetime, timedelta

load_dotenv()

DB_USER = os.environ["POSTGRES_USER"]
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DB_PORT = os.environ["POSTGRES_PORT"]
DB_NAME = os.environ["POSTGRES_DB"]

# Create a connection URL using the configuration values
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost:{DB_PORT}/{DB_NAME}"

# Create a database engine
engine = create_engine(DATABASE_URL)

# Connect to the database
session = sessionmaker(bind=engine)()

# Calculate the time range
now = datetime.utcnow()
one_hour_ago = now - timedelta(hours=1)

# Fetch the liquidations in the last hour
liquidations_last_hour = (
    session.query(Liquidation)
    .filter(Liquidation.event_time.between(one_hour_ago, now))
    .all()
)


# last_10_liquidations = (
#     session.query(Liquidation)
#     .filter(Liquidation.price * Liquidation.quantity > 1000)
#     .order_by(Liquidation.id.desc())
#     .limit(10)
#     .all()
# )


df = pd.DataFrame([vars(l) for l in liquidations_last_hour])
print(df)


last_10_liquidations = (
    session.query(Liquidation).order_by(Liquidation.id.desc()).limit(10).all()
)
df = pd.DataFrame([vars(l) for l in last_10_liquidations])
print(df)

session.close()
