
import json

from .database import (
    SessionLocal,
    engine
)

from .models import (
    Base,
    Event
)

Base.metadata.create_all(
    bind=engine
)

db = SessionLocal()

with open(
    "events.jsonl",
    "r"
) as f:

    for line in f:

        data = json.loads(
            line
        )

        event = Event(
            event_id=data["event_id"],
            visitor_id=data["visitor_id"],
            event_type=data["event_type"],
            camera_id=data["camera_id"],
            zone=data.get("zone"),
            confidence=data["confidence"],
            timestamp=data["timestamp"]
        )

        db.add(event)

db.commit()

print("Events Imported")