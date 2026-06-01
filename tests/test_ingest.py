import uuid
from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json().get('status') == 'ok'

def test_ingest_idempotent():
    ev_id = str(uuid.uuid4())
    payload = [{
        'event_id': ev_id,
        'event_type': 'ENTRY',
        'store_id': 'store_test',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'is_staff': False,
        'confidence': 0.95,
        'metadata': {'foo': 'bar'},
        'camera_id': 'cam_test'
    }]
    r1 = client.post('/events/ingest', json=payload)
    assert r1.status_code == 200
    j1 = r1.json()
    assert j1['inserted'] == 1
    # send again - should be ignored
    r2 = client.post('/events/ingest', json=payload)
    assert r2.status_code == 200
    j2 = r2.json()
    assert j2['inserted'] == 0
    assert j2['ignored'] >= 1
