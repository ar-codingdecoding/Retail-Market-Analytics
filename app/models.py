from sqlalchemy import (
    Column,
    Integer,
    String,
    Float
)

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Event(Base):

    __tablename__ = "events"

    id = Column(
        Integer,
        primary_key=True
    )

    event_id = Column(String)

    store_id = Column(String)

    visitor_id = Column(String)

    event_type = Column(String)

    camera_id = Column(String)

    zone_id = Column(String)

    confidence = Column(Float)

    timestamp = Column(String)