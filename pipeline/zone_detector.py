class ZoneDetector:

    def __init__(self, zones):
        self.zones = zones

    def get_zone(self, x, y):

        # Ignore border region between DISPLAY and MAKEUP
        if 670 <= x <= 730:
            return None

        for zone_name, box in self.zones.items():

            x1, y1, x2, y2 = box

            if (
                x1 <= x <= x2
                and
                y1 <= y <= y2
            ):
                return zone_name

        return None