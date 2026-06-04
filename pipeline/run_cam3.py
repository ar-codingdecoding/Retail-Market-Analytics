from ultralytics import YOLO
import supervision as sv
import cv2

from line_counter import LineCounter
from event_generator import EventGenerator
from event_store import EventStore


# --------------------------
# CONFIG
# --------------------------

VIDEO_PATH = "data/videos/CAM 3.mp4"

LINE_Y = 300

SHOW_WINDOW = True


# --------------------------
# INIT
# --------------------------

print("Loading YOLO...")

model = YOLO("yolo11s.pt")

print("Creating ByteTrack...")

tracker = sv.ByteTrack(
    track_activation_threshold=0.35,
    lost_track_buffer=120,
    minimum_matching_threshold=0.95,
    frame_rate=30
)

print("Creating Event Store...")

event_store = EventStore()

line_counter = LineCounter(
    line_y=LINE_Y
)

print("Opening Video...")

cap = cv2.VideoCapture(
    VIDEO_PATH
)

if not cap.isOpened():

    print("Failed to open video.")

    exit()


# --------------------------
# PROCESS LOOP
# --------------------------




frame_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        print("Video completed.")
        break

    frame_count += 1

    result = model(
        frame,
        verbose=False
    )[0]

    detections = sv.Detections.from_ultralytics(
        result
    )

    if len(detections) > 0:
        detections = detections[
            detections.class_id == 0
        ]

        detections = tracker.update_with_detections(
            detections
        )

        # Draw Entry Line
        cv2.line(
            frame,
            (0, LINE_Y),
            (frame.shape[1], LINE_Y),
            (0, 255, 0),
            3
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
                event_type = line_counter.check_crossing(
                    track_id,
                    center_y
                )
                # Event Found
                if event_type:
                    event = EventGenerator.generate(
                        visitor_id=track_id,
                        event_type=event_type,
                        camera_id="CAM3",
                        confidence=1.0
                    )
                    event_store.save(
                        event
                    )
                    print(
                        f"[EVENT] {event}"
                    )
                # Bounding Box
                cv2.rectangle(
                    frame,
                    (int(x1), int(y1)),
                    (int(x2), int(y2)),
                    (0, 255, 0),
                    2
                )
                # Tracker ID
                cv2.putText(
                    frame,
                    f"ID {track_id}",
                    (int(x1), int(y1)-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )
                # Center Point
                cv2.circle(
                    frame,
                    (center_x, center_y),
                    4,
                    (0, 0, 255),
                    -1
                )

    if SHOW_WINDOW:
        cv2.imshow(
            "Store Intelligence",
            frame
        )
        key = cv2.waitKey(1)
        if key == 27:
            break

cap.release()
cv2.destroyAllWindows()
print("Finished.")