import time


class EventDeduplicator:

    def __init__(self):

        self.generated = {}

        self.expiry_seconds = 30

    def should_save(
        self,
        visitor_id,
        event_type,
        zone=None
    ):

        now = time.time()

        # cleanup old entries

        expired = []

        for key, timestamp in self.generated.items():

            if now - timestamp > self.expiry_seconds:

                expired.append(key)

        for key in expired:

            del self.generated[key]

        key = (
            visitor_id,
            event_type,
            zone
        )

        if key in self.generated:

            return False

        self.generated[key] = now

        return True