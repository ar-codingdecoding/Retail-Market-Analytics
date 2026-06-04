from app.database import SessionLocal
from app.models import Event


def get_metrics(store_id: str):
    # print("Received:", store_id)
    db = SessionLocal()
    if store_id == "ALL_STORE2":

        cameras = [
            "STORE2_CAM1",
            "STORE2_CAM2",
            "STORE2_CAM6"
        ]

        total_events = db.query(Event).filter(
            Event.camera_id.in_(cameras)
        ).count()

        zone_enter = db.query(Event).filter(
            Event.event_type == "ZONE_ENTER",
            Event.camera_id.in_(cameras)
        ).count()

        zone_dwell = db.query(Event).filter(
            Event.event_type == "ZONE_DWELL",
            Event.camera_id.in_(cameras)
        ).count()

    # -------------------------
    # SINGLE CAMERA
    # -------------------------

    else:

        total_events = db.query(Event).filter(
            Event.camera_id == store_id
        ).count()

        zone_enter = db.query(Event).filter(
            Event.event_type == "ZONE_ENTER",
            Event.camera_id == store_id
        ).count()

        zone_dwell = db.query(Event).filter(
            Event.event_type == "ZONE_DWELL",
            Event.camera_id == store_id
        ).count()

    db.close()

    return {
        "total_events": total_events,
        "zone_enter_events": zone_enter,
        "zone_dwell_events": zone_dwell
    }


def get_heatmap(store_id: str):

    db = SessionLocal()

    if store_id == "ALL_STORE2":

        cameras = [
            "STORE2_CAM1",
            "STORE2_CAM2",
            "STORE2_CAM6"
        ]

        rows = db.query(Event).filter(
            Event.camera_id.in_(cameras)
        ).all()

    elif store_id == "ALL_STORE1":

        cameras = [
            "CAM1",
            "CAM2",
            "CAM3",
            "CAM5"
        ]

        rows = db.query(Event).filter(
            Event.camera_id.in_(cameras)
        ).all()

    else:

        rows = db.query(Event).filter(
            Event.camera_id == store_id
        ).all()

    zone_counts = {}

    unique_visitors = set()

    for row in rows:

        if row.visitor_id:
            unique_visitors.add(
                row.visitor_id
            )

        zone = row.zone_id

        if not zone:
            continue

        zone_counts[zone] = (
            zone_counts.get(zone, 0) + 1
        )

    db.close()

    if len(zone_counts) == 0:

        return {
            "zones": {},
            "data_confidence": False
        }

    max_visits = max(
        zone_counts.values()
    )

    normalized = {}

    for zone, visits in zone_counts.items():

        score = round(
            (visits / max_visits) * 100,
            2
        )

        normalized[zone] = {
            "visits": visits,
            "score": score
        }

    return {
        "zones": normalized,
        "data_confidence":
            len(unique_visitors) >= 20,
        "unique_visitors":
            len(unique_visitors)
    }


def get_funnel(store_id: str):

    db = SessionLocal()

    if store_id == "ALL_STORE2":

        cameras = [
            "STORE2_CAM1",
            "STORE2_CAM2",
            "STORE2_CAM6"
        ]

        entered = db.query(Event).filter(
            Event.event_type == "ZONE_ENTER",
            Event.camera_id.in_(cameras)
        ).count()

        dwell = db.query(Event).filter(
            Event.event_type == "ZONE_DWELL",
            Event.camera_id.in_(cameras)
        ).count()

    elif store_id == "ALL_STORE1":

        cameras = [
            "CAM1",
            "CAM2",
            "CAM3",
            "CAM5"
        ]

        entered = db.query(Event).filter(
            Event.event_type == "ZONE_ENTER",
            Event.camera_id.in_(cameras)
        ).count()

        dwell = db.query(Event).filter(
            Event.event_type == "ZONE_DWELL",
            Event.camera_id.in_(cameras)
        ).count()

    else:

        entered = db.query(Event).filter(
            Event.event_type == "ZONE_ENTER",
            Event.camera_id == store_id
        ).count()

        dwell = db.query(Event).filter(
            Event.event_type == "ZONE_DWELL",
            Event.camera_id == store_id
        ).count()

    db.close()

    conversion = 0

    if entered > 0:

        conversion = (
            dwell / entered
        ) * 100

    return {
        "entered": entered,
        "engaged": dwell,
        "conversion_rate": round(
            conversion,
            2
        )
    }


def ingest_events(data):

    if not isinstance(data, list):

        data = [data]

    if len(data) > 500:

        return {
            "status": "error",
            "message": "Maximum 500 events allowed per request"
        }

    db = SessionLocal()

    success = 0
    duplicate = 0

    errors = []

    required_fields = [
        "event_id",
        "visitor_id",
        "event_type",
        "camera_id",
        "confidence",
        "timestamp"
    ]

    for index, event in enumerate(data):

        try:

            for field in required_fields:

                if field not in event:

                    errors.append({
                        "index": index,
                        "error": f"Missing field: {field}"
                    })

                    raise ValueError()

            existing = db.query(Event).filter(
                Event.event_id == event["event_id"]
            ).first()

            if existing:

                duplicate += 1

                continue

            db.add(
                Event(
                    event_id=event["event_id"],
                    visitor_id=event["visitor_id"],
                    event_type=event["event_type"],
                    camera_id=event["camera_id"],
                    zone=event.get("zone"),
                    confidence=float(
                        event["confidence"]
                    ),
                    timestamp=event["timestamp"]
                )
            )

            success += 1

        except Exception:

            continue

    db.commit()

    db.close()

    return {

        "status":
            "partial_success"
            if len(errors) > 0
            else "success",

        "received":
            len(data),

        "inserted":
            success,

        "duplicates":
            duplicate,

        "failed":
            len(errors),

        "errors":
            errors
    }


def get_anomalies(store_id: str):

    db = SessionLocal()

    if store_id == "ALL_STORE2":

        cameras = [
            "STORE2_CAM1",
            "STORE2_CAM2",
            "STORE2_CAM6"
        ]

        total_events = db.query(Event).filter(
            Event.camera_id.in_(cameras)
        ).count()

    elif store_id == "ALL_STORE1":

        cameras = [
            "CAM1",
            "CAM2",
            "CAM3",
            "CAM5"
        ]

        total_events = db.query(Event).filter(
            Event.camera_id.in_(cameras)
        ).count()

    else:

        total_events = db.query(Event).filter(
            Event.camera_id == store_id
        ).count()

    anomalies = []

    if total_events == 0:

        anomalies.append({
            "severity": "WARN",
            "type": "DEAD_ZONE",
            "message": "No visitor activity detected"
        })

    db.close()

    return {
        "anomalies": anomalies
    }