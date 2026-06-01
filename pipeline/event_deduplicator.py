class EventDeduplicator:

    def __init__(self):

        self.generated = set()

    def should_save(
        self,
        visitor_id,
        event_type,
        zone=None
    ):

        # Allow repeated dwell events

        if event_type == "ZONE_DWELL":
            return True

        key = (
            visitor_id,
            event_type,
            zone
        )

        if key in self.generated:
            return False

        self.generated.add(key)

        return True