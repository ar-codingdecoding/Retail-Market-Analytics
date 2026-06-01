from collections import defaultdict
from datetime import datetime


class ZoneTracker:

    def __init__(self):

        self.current_zone = defaultdict(lambda: None)

        self.entry_time = {}

        self.last_seen = {}

        self.exit_timeout = 3

        # every 30 sec dwell
        self.last_dwell_emit = {}

    def update(
        self,
        visitor_id,
        zone_name
    ):

        now = datetime.now()

        self.last_seen[visitor_id] = now

        previous_zone = self.current_zone[visitor_id]

        # -------------------------
        # FIRST ENTRY
        # -------------------------

        if previous_zone is None and zone_name is not None:

            self.current_zone[visitor_id] = zone_name

            self.entry_time[visitor_id] = now

            self.last_dwell_emit[visitor_id] = 0

            return (
                "ZONE_ENTER",
                zone_name
            )

        # -------------------------
        # ZONE CHANGE
        # -------------------------

        if (
            previous_zone is not None
            and zone_name is not None
            and previous_zone != zone_name
        ):

            self.current_zone[visitor_id] = zone_name

            self.entry_time[visitor_id] = now

            self.last_dwell_emit[visitor_id] = 0

            return (
                "ZONE_ENTER",
                zone_name
            )

        # -------------------------
        # CONTINUOUS DWELL
        # emit every 30 sec
        # -------------------------

        if (
            previous_zone is not None
            and visitor_id in self.entry_time
        ):

            duration = (
                now -
                self.entry_time[visitor_id]
            ).total_seconds()

            last_emit = self.last_dwell_emit.get(
                visitor_id,
                0
            )

            if duration >= (last_emit + 30):

                self.last_dwell_emit[
                    visitor_id
                ] = int(duration)

                return (
                    "ZONE_DWELL",
                    previous_zone
                )

        return None

    # -------------------------
    # EXIT CLEANUP
    # -------------------------

    def cleanup_exits(self):

        now = datetime.now()

        exits = []

        for visitor_id in list(
            self.last_seen.keys()
        ):

            seconds = (
                now -
                self.last_seen[visitor_id]
            ).total_seconds()

            if seconds > self.exit_timeout:

                zone = self.current_zone[
                    visitor_id
                ]

                if zone:

                    exits.append(
                        (
                            visitor_id,
                            zone
                        )
                    )

                self.current_zone.pop(
                    visitor_id,
                    None
                )

                self.entry_time.pop(
                    visitor_id,
                    None
                )

                self.last_seen.pop(
                    visitor_id,
                    None
                )

                self.last_dwell_emit.pop(
                    visitor_id,
                    None
                )

        return exits