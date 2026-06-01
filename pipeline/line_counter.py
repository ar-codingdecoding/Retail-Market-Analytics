from collections import defaultdict
from datetime import datetime


class LineCounter:

    def __init__(self, line_y):

        self.line_y = line_y

        self.previous_y = defaultdict(
            lambda: None
        )

        self.last_event = {}

        self.last_event_time = {}

        self.buffer = 30

        self.cooldown_seconds = 3

    def check_crossing(
        self,
        track_id,
        center_y
    ):

        previous = self.previous_y[
            track_id
        ]

        self.previous_y[
            track_id
        ] = center_y

        if previous is None:
            return None

        now = datetime.now()

        # Cooldown

        if track_id in self.last_event_time:

            seconds = (
                now -
                self.last_event_time[
                    track_id
                ]
            ).total_seconds()

            if seconds < self.cooldown_seconds:
                return None

        # ENTRY

        if (
            previous < (
                self.line_y - self.buffer
            )
            and
            center_y > (
                self.line_y + self.buffer
            )
        ):

            if self.last_event.get(
                track_id
            ) != "ENTRY":

                self.last_event[
                    track_id
                ] = "ENTRY"

                self.last_event_time[
                    track_id
                ] = now

                return "ENTRY"

        # EXIT

        if (
            previous > (
                self.line_y + self.buffer
            )
            and
            center_y < (
                self.line_y - self.buffer
            )
        ):

            if self.last_event.get(
                track_id
            ) != "EXIT":

                self.last_event[
                    track_id
                ] = "EXIT"

                self.last_event_time[
                    track_id
                ] = now

                return "EXIT"

        return None