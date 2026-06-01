from datetime import datetime


class ReIDManager:

    def __init__(self):

        self.exited_people = {}

        self.reentry_window = 60

    def save_exit(
        self,
        visitor_id,
        center_x,
        center_y
    ):

        self.exited_people[
            visitor_id
        ] = {
            "x": center_x,
            "y": center_y,
            "time": datetime.now()
        }

    def check_reentry(
        self,
        center_x,
        center_y
    ):

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

            distance = (
                (center_x - data["x"]) ** 2 +
                (center_y - data["y"]) ** 2
            ) ** 0.5

            if distance < 150:

                return visitor_id

        return None