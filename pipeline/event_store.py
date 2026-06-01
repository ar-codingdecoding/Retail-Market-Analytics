import json
import os


class EventStore:

    def __init__(self):

        self.file_path = "events.jsonl"

        if not os.path.exists(self.file_path):
            open(self.file_path, "w").close()

    def save(self, event):

        with open(
            self.file_path,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                json.dumps(event)
            )

            f.write("\n")