import json
import os
import sqlite3


class EventStore:

    def __init__(self):

        self.file_path = "events.jsonl"

        self.db_path = "store_intelligence.db"

        if not os.path.exists(
            self.file_path
        ):
            open(
                self.file_path,
                "w"
            ).close()

    def save(
        self,
        event
    ):

        # -------------------
        # JSONL
        # -------------------

        with open(
            self.file_path,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                json.dumps(event)
            )

            f.write("\n")

        # -------------------
        # SQLITE
        # -------------------

        try:

            conn = sqlite3.connect(
                self.db_path
            )

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO events
                (
                    event_id,
                    store_id,
                    visitor_id,
                    event_type,
                    camera_id,
                    zone_id,
                    confidence,
                    timestamp
                )
                VALUES
                (?, ?, ?, ?, ?, ?, ?, ?)
                """,
               (
                event["event_id"],
                event.get(
                    "store_id",
                    "STORE_1"
                ),
                str(
                    event["visitor_id"]
                ),
                event["event_type"],
                event["camera_id"],
                event.get(
                    "zone"
                ),
                float(
                    event["confidence"]
                ),
                event["timestamp"]
            )
            )

            conn.commit()

            conn.close()

        except Exception as e:

            print(
                "DB INSERT ERROR:",
                e
            )