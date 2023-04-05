from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Declare the base class for the ORM models
Base = declarative_base()

# Liquidation table
class Liquidation(Base):
    __tablename__ = "liquidations"

    id = Column(Integer, primary_key=True)
    event_type = Column(String)
    event_time = Column(DateTime)
    symbol = Column(String)
    side = Column(String)
    order_type = Column(String)
    time_in_force = Column(String)
    quantity = Column(String)
    price = Column(String)
    average_price = Column(String)
    order_status = Column(String)
    last_filled_quantity = Column(String)
    filled_accumulated_quantity = Column(String)
    order_trade_time = Column(DateTime)
    received_timestamp = Column(DateTime, nullable=False)

"""
WebSocket error: (psycopg2.errors.DatatypeMismatch) column "event_time" is of type timestamp without time zone but expression is of type bigint
"""
