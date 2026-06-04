import subprocess
import sys
import os

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

processes = []

camera_files = [
    "run_cam1.py",
    "run_cam2.py",
    "run_cam3.py",
    "run_cam5.py"
]

try:

    for file in camera_files:

        path = os.path.join(
            BASE_DIR,
            file
        )

        print(
            f"Starting {file}"
        )

        p = subprocess.Popen(
            [sys.executable, path]
        )

        processes.append(
            p
        )

    print(
        "\nAll camera pipelines started."
    )

    for p in processes:
        p.wait()

except KeyboardInterrupt:

    print(
        "\nStopping all cameras..."
    )

    for p in processes:

        p.terminate()

    print(
        "All cameras stopped."
    )