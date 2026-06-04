from datetime import datetime

import cv2


class ReIDManager:

    def __init__(self):

        self.exited_people = {}

        self.reentry_window = 60

    def save_exit(
        self,
        visitor_id,
        center_x,
        center_y,
        histogram
    ):

        self.exited_people[
            visitor_id
        ] = {
            "x": center_x,
            "y": center_y,
            "time": datetime.now(),
            "hist": histogram
        }

    def check_reentry(
        self,
        center_x,
        center_y,
        histogram
    ):

        if histogram is None:
            return None

        now = datetime.now()

        for visitor_id, data in list(
            self.exited_people.items()
        ):

            age = (
                now - data["time"]
            ).total_seconds()

            if age > self.reentry_window:

                self.exited_people.pop(
                    visitor_id,
                    None
                )

                continue

            if data["hist"] is None:
                continue

            distance = (
                (center_x - data["x"]) ** 2 +
                (center_y - data["y"]) ** 2
            ) ** 0.5

            score = cv2.compareHist(
                histogram,
                data["hist"],
                cv2.HISTCMP_CORREL
            )

            if distance < 100 and score > 0.90:

                self.exited_people.pop(
                    visitor_id,
                    None
                )
                print(
                    f"RE-ID MATCH -> old={visitor_id} "
                    f"distance={distance:.1f} "
                    f"score={score:.2f}"
                )
                return visitor_id

        return None