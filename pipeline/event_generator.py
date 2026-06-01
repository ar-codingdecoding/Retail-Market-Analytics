from datetime import datetime
from uuid import uuid4


class EventGenerator:

    @staticmethod
    def generate(
        visitor_id,
        event_type,
        camera_id,
        zone=None,
        confidence=1.0
    ):

        return {
            "event_id": str(uuid4()),
            "visitor_id": str(visitor_id),
            "event_type": event_type,
            "camera_id": camera_id,
            "zone": zone,
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat()
        }