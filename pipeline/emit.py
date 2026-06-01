"""Emit sample events to the Store Intelligence API.
Usage: python emit.py --host http://localhost:8000
"""
import argparse
import json
import requests
from pathlib import Path

def emit(file_path: str, host: str):
    url = host.rstrip('/') + '/events/ingest'
    with open(file_path, 'r') as fh:
        lines = [json.loads(l) for l in fh if l.strip()]
    # send as batch
    resp = requests.post(url, json=lines)
    print('status', resp.status_code)
    try:
        print(resp.json())
    except Exception:
        print(resp.text)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--file', default='sample_events.jsonl')
    p.add_argument('--host', default='http://localhost:8000')
    args = p.parse_args()
    emit(args.file, args.host)
