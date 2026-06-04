# Retail Market Analytics – Store Intelligence Platform

## Overview

Retail Market Analytics is a multi-camera retail intelligence platform that converts CCTV footage into actionable business insights. The system processes customer movement events from different store zones and generates analytics for store operations, customer engagement, and decision-making.

The solution was developed for the Purplle Tech Challenge 2026.

---

## Problem Statement

Retail stores generate large amounts of video data through CCTV systems. Manually analyzing customer behavior, zone engagement, and store traffic is difficult and not scalable.

This project provides an automated analytics pipeline that:

* Tracks customer movement across store zones
* Measures engagement and dwell behavior
* Generates funnel analytics
* Detects anomalies in store activity
* Produces heatmap-style zone popularity insights
* Exposes analytics through APIs and an interactive dashboard

---

## Features

### Customer Analytics

* Unique visitor estimation
* Customer movement tracking
* Zone entry detection
* Dwell-time monitoring

### Business Intelligence

* Conversion funnel analytics
* Store performance metrics
* Zone popularity analysis
* Customer engagement measurement

### Monitoring

* Anomaly detection
* Real-time event ingestion
* Health monitoring API

### Visualization

* Interactive dashboard
* Funnel charts
* Traffic heatmaps
* Store-wise and camera-wise analytics

---

## System Architecture

CCTV Streams
↓
Detection & Tracking Pipeline
↓
Event Generation
↓
Event Deduplication
↓
SQLite Event Store
↓
FastAPI Analytics Service
↓
Streamlit Dashboard

---

## Technology Stack

### Computer Vision

* YOLO (Ultralytics)
* OpenCV
* Supervision

### Backend

* FastAPI
* SQLAlchemy
* SQLite

### Dashboard

* Streamlit
* Plotly
* Pandas

### Deployment

* Docker
* Render
* Streamlit Community Cloud

---

## Repository Structure

## Repository Structure

```text
STORE-INTELLIGENCE/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── ingest.py
│   ├── main.py
│   ├── models.py
│   └── services.py
│
├── dashboard/
│   └── app.py
│
├── pipeline/
│   ├── emit.py
│   ├── event_deduplicator.py
│   ├── event_generator.py
│   ├── event_store.py
│   ├── event_types.py
│   ├── events.py
│   ├── line_counter.py
│   ├── reid_manager.py
│   ├── tracker.py
│   ├── zone_detector.py
│   ├── zone_tracker.py
│   ├── zones.py
│   ├── staff_detector.py
│   ├── main.py
│   │
│   ├── run_cam1.py
│   ├── run_cam2.py
│   ├── run_cam3.py
│   ├── run_cam5.py
│   │
│   ├── store2_cam1.py
│   ├── store2_cam2.py
│   ├── store2_cam6.py
│   │
│   ├── zones_cam5.py
│   └── zones_store2.py
│
├── data/
│   └── videos/
│
├── tests/
│
├── CHOICES.md
├── DESIGN.md
├── README.md
│
├── sample_events.jsonl
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
│
├── .gitignore
├── .dockerignore
└── .gitattributes
```


---

## Live Deployment

### Dashboard

https://ar-codingdecoding-retail-market-analytics-dashboardapp-ppwlh6.streamlit.app/

### API

https://store-intelligence-api-qkiu.onrender.com

### Swagger UI

https://store-intelligence-api-qkiu.onrender.com/docs

---

## API Endpoints

### Health Check

```http
GET /health
```

### Metrics

```http
GET /stores/{store_id}/metrics
```

### Funnel Analytics

```http
GET /stores/{store_id}/funnel
```

### Heatmap Analytics

```http
GET /stores/{store_id}/heatmap
```

### Anomaly Detection

```http
GET /stores/{store_id}/anomalies
```

### Event Ingestion

```http
POST /events/ingest
```

---

## Local Setup

### Clone Repository

```bash
git clone https://github.com/ar-codingdecoding/Retail-Market-Analytics.git
cd Retail-Market-Analytics
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows

```bash
.venv\Scripts\activate
```

Linux/Mac

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run API

```bash
uvicorn app.main:app --reload
```

### Run Dashboard

```bash
streamlit run dashboard/app.py
```

---

## Docker Deployment

Build Image

```bash
docker compose build
```

Run Containers

```bash
docker compose up
```

API will be available at:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

## Assumptions

* Event data is generated from processed CCTV streams.
* Sample event data is provided for demonstration.
* SQLite is used for lightweight deployment and evaluation.
* Analytics are computed from stored event records.

---

## Documentation

Additional technical documentation is available in:

* docs/DESIGN.md
* docs/CHOICES.md

---

## Authors

Ajay Raj
Email-id: ar.bppimt2022@gmail.com
B.Tech Final Year
Retail Market Analytics – Purplle Tech Challenge 2026 Submission
