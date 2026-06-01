from uuid import uuid4
from datetime import datetime

def create_event(
    visitor_id,
    event_type,
    camera_id
):

    return {
        "event_id": str(uuid4()),
        "visitor_id": visitor_id,
        "event_type": event_type,
        "camera_id": camera_id,
        "timestamp": datetime.utcnow().isoformat()
    }