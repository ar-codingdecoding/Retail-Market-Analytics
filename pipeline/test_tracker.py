from ultralytics import YOLO
import supervision as sv
import cv2

model = YOLO("yolo11s.pt")

tracker = sv.ByteTrack()

cap = cv2.VideoCapture(
    "data/videos/CAM 3.mp4"
)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    result = model(frame)[0]

    detections = sv.Detections.from_ultralytics(
        result
    )

    detections = tracker.update_with_detections(
        detections
    )

    if detections.tracker_id is not None:

        for i, track_id in enumerate(
            detections.tracker_id
        ):

            x1, y1, x2, y2 = detections.xyxy[i]

            cv2.rectangle(
                frame,
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                (0,255,0),
                2
            )

            cv2.putText(
                frame,
                f"ID {track_id}",
                (int(x1), int(y1)-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0,255,0),
                2
            )

    cv2.imshow(
        "Tracking",
        frame
    )

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()