import cv2


class StaffDetector:

    def is_staff(self, roi):

        if roi.size == 0:
            return False

        hsv = cv2.cvtColor(
            roi,
            cv2.COLOR_BGR2HSV
        )

        pink_mask = cv2.inRange(
            hsv,
            (140, 40, 40),
            (180, 255, 255)
        )

        pink_pixels = cv2.countNonZero(
            pink_mask
        )

        total_pixels = (
            roi.shape[0]
            *
            roi.shape[1]
        )

        ratio = pink_pixels / max(
            total_pixels,
            1
        )

        return ratio > 0.15