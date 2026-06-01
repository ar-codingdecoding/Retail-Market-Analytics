from ultralytics import YOLO
import cv2

model = YOLO("yolo11s.pt")

cap = cv2.VideoCapture("data/videos/CAM 1.mp4")
print("Video opened:", cap.isOpened())
ret, frame = cap.read()
print("Frame read:", ret)
while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame)

    annotated = results[0].plot()

    cv2.imshow("Detection", annotated)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()