from ultralytics import YOLO
import supervision as sv
import cv2

from zones import CAM2_ZONES
from zone_detector import ZoneDetector
from zone_tracker import ZoneTracker
from reid_manager import ReIDManager
from event_generator import EventGenerator
from event_store import EventStore
from event_deduplicator import EventDeduplicator


# -----------------------------
# TV REGION (IGNORE)
# -----------------------------

TV_REGION = (
    0,
    0,
    450,
    300
)

STAFF_REGION = (
    1500,
    300,
    1920,
    1080
)
def is_staff(center_x, center_y):

    x1, y1, x2, y2 = STAFF_REGION

    return (
        x1 <= center_x <= x2
        and
        y1 <= center_y <= y2
    )

# -----------------------------
# INIT
# -----------------------------

model = YOLO("yolo11s.pt")

tracker = sv.ByteTrack(
    track_activation_threshold=0.35,
    lost_track_buffer=120,
    minimum_matching_threshold=0.95,
    frame_rate=30
)

zone_detector = ZoneDetector(
    CAM2_ZONES
)
reid_manager = ReIDManager()
zone_tracker = ZoneTracker()

event_store = EventStore()

deduplicator = EventDeduplicator()

cap = cv2.VideoCapture(
    "data/videos/CAM 2.mp4"
)

if not cap.isOpened():

    print("Cannot open video")
    exit()

# -----------------------------
# LOOP
# -----------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        break

    result = model(
        frame,
        verbose=False
    )[0]

    detections = sv.Detections.from_ultralytics(
        result
    )

    # PERSON ONLY

    if len(detections) > 0:

        detections = detections[
            detections.class_id == 0
        ]

        detections = detections[
            detections.confidence > 0.50
        ]

        valid_indices = []

        for i, box in enumerate(
            detections.xyxy
        ):

            x1, y1, x2, y2 = box

            width = x2 - x1
            height = y2 - y1

            if (
                width > 40
                and
                height > 100
            ):
                valid_indices.append(i)

        detections = detections[
            valid_indices
        ]

    detections = tracker.update_with_detections(
        detections
    )

    # DRAW ZONES

    for zone_name, box in CAM2_ZONES.items():

        x1, y1, x2, y2 = box

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            zone_name,
            (x1 + 20, y1 + 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2
        )

    sx1, sy1, sx2, sy2 = STAFF_REGION

    cv2.rectangle(
        frame,
        (sx1, sy1),
        (sx2, sy2),
        (0, 0, 255),
        2
    )

    cv2.putText(
        frame,
        "STAFF AREA",
        (sx1 + 20, sy1 + 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    if detections.tracker_id is not None:

        for i, track_id in enumerate(
            detections.tracker_id
        ):

            x1, y1, x2, y2 = detections.xyxy[i]

            center_x = int(
                (x1 + x2) / 2
            )

            center_y = int(
                (y1 + y2) / 2
            )

            old_id = reid_manager.check_reentry(
                center_x,
                center_y
            )

            if old_id is not None:
                track_id = old_id

            # -----------------------------
            # IGNORE TV
            # -----------------------------

            tx1, ty1, tx2, ty2 = TV_REGION

            if (
                tx1 <= center_x <= tx2
                and
                ty1 <= center_y <= ty2
            ):
                continue
            if is_staff(
                center_x,
                center_y
            ):
                continue
            zone = zone_detector.get_zone(
                center_x,
                center_y
            )

            event = zone_tracker.update(
                track_id,
                zone
            )

            if event:

                event_type, zone_name = event

                if deduplicator.should_save(
                    track_id,
                    event_type
                ):

                    data = EventGenerator.generate(
                        visitor_id=track_id,
                        event_type=event_type,
                        camera_id="CAM2",
                        zone=zone_name
                    )

                    event_store.save(
                        data
                    )

                    print(data)

            # DRAW BOX

            cv2.rectangle(
                frame,
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"ID {track_id}",
                (
                    int(x1),
                    int(y1) - 10
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.circle(
                frame,
                (
                    center_x,
                    center_y
                ),
                5,
                (0, 0, 255),
                -1
            )

            if zone:

                cv2.putText(
                    frame,
                    zone,
                    (
                        center_x,
                        center_y - 15
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2
                )

    exits = zone_tracker.cleanup_exits()

    for visitor_id, zone_name in exits:

        if deduplicator.should_save(
            visitor_id,
            "ZONE_EXIT",
            zone_name
        ):

            data = EventGenerator.generate(
                visitor_id=visitor_id,
                event_type="ZONE_EXIT",
                camera_id="CAM2",
                zone=zone_name
            )

            event_store.save(
                data
            )

            print(data)

    cv2.imshow(
        "CAM2",
        frame
    )

    if cv2.waitKey(1) == 27:
        break

cap.release()

cv2.destroyAllWindows()