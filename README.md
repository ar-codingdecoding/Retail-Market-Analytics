# Store Intelligence System

AI-powered retail analytics platform built using CCTV footage, computer vision, event-driven architecture, and real-time analytics APIs.

---

# Overview

This project converts raw CCTV footage into actionable retail intelligence.

The system:

* Detects customers using YOLO11
* Tracks visitors using ByteTrack
* Detects zone interactions
* Generates behavioral events
* Stores events in SQLite
* Exposes analytics through FastAPI
* Visualizes metrics through a dashboard

---

# Features

## Detection Pipeline

* Person Detection (YOLO11s)
* Multi-Object Tracking (ByteTrack)
* Zone Classification
* Zone Enter Events
* Zone Exit Events
* Zone Dwell Events

---

## Analytics API

### Health

```http
GET /health
```

Returns service status.

---

### Event Ingestion

```http
POST /events/ingest
```

Features:

* Batch ingestion
* Deduplication
* Partial success handling
* Event validation

---

### Metrics

```http
GET /stores/{store_id}/metrics
```

Returns:

* Total Events
* Zone Entries
* Dwell Events

---

### Funnel

```http
GET /stores/{store_id}/funnel
```

Returns visitor engagement funnel.

---

### Heatmap

```http
GET /stores/{store_id}/heatmap
```

Returns:

* Zone popularity
* Normalized scores (0–100)
* Data confidence indicator

---

### Anomalies

```http
GET /stores/{store_id}/anomalies
```

Returns detected operational anomalies.

---

# Project Structure

```text
store-intelligence/

├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── services.py
│
├── pipeline/
│   ├── run_cam1.py
│   ├── run_cam2.py
│   ├── zone_detector.py
│   ├── zone_tracker.py
│   └── zones.py
│
├── dashboard/
│   └── dashboard.py
│
├── docs/
│   ├── DESIGN.md
│   └── CHOICES.md
│
├── events.jsonl
├── retail.db
├── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <repository_url>
cd store-intelligence
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running Detection Pipeline

CAM1

```bash
python pipeline/run_cam1.py
```

CAM2

```bash
python pipeline/run_cam2.py
```

Generated events are written to:

```text
events.jsonl
```

---

# Import Events Into Database

```bash
python -m app.ingest
```

This populates:

```text
retail.db
```

---

# Run API

```bash
uvicorn app.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# Run Dashboard

```bash
streamlit run dashboard/dashboard.py
```

Dashboard URL:

```text
http://localhost:8501
```

---

# Event Schema

Example:

```json
{
  "event_id": "uuid",
  "visitor_id": "5",
  "event_type": "ZONE_ENTER",
  "camera_id": "CAM2",
  "zone": "DISPLAY",
  "confidence": 1.0,
  "timestamp": "2026-06-01T15:51:02"
}
```

---

# Known Limitations

## Staff Detection

A fixed-region and rule-based approach was evaluated but not enabled by default due to overlap between customer and staff movement patterns.

---

## Re-Identification

A lightweight ReID prototype was explored. A production-grade implementation would require appearance embeddings and a labeled identity dataset.

---

# Future Improvements

* DeepSORT / StrongSORT
* Person ReID embeddings
* Billing Queue Analytics
* POS Correlation
* Kafka Event Streaming
* PostgreSQL Backend
* Multi-Camera Tracking
* WebSocket Live Updates

---

# Technologies Used

* Python
* OpenCV
* YOLO11s
* ByteTrack
* FastAPI
* SQLite
* Streamlit

---

# Conclusion

The Store Intelligence System demonstrates an end-to-end pipeline that transforms CCTV footage into real-time retail analytics through detection, tracking, event generation, analytics APIs, anomaly detection, and dashboard visualization.
