# DESIGN.md

# Retail Market Analytics System Design

## Overview

This solution processes multi-camera retail CCTV footage to generate structured retail analytics events. The system performs customer detection, tracking, re-identification, zone analytics, dwell-time measurement, entry/exit counting, staff exclusion, and anomaly detection.

The architecture is designed as a modular pipeline that can process multiple camera streams independently while producing a unified analytics layer.

---

# System Architecture

```text
CCTV Video Streams
        |
        v
Person Detection (YOLO11s)
        |
        v
Multi-Object Tracking
        |
        v
Person Re-Identification
        |
        v
Staff Exclusion
        |
        v
Zone & Line Analytics
        |
        v
Event Generation
        |
        v
JSONL Event Log
        |
        v
FastAPI Analytics Service
        |
        v
Streamlit Dashboard
```

---

# Detection Layer

The system uses YOLO11s for person detection.

Responsibilities:

* Detect people in video frames
* Provide bounding boxes
* Maintain real-time processing capability
* Support multiple camera views

Only the person class is used for analytics generation.

---

# Tracking Layer

A tracker assigns temporary IDs to detected customers.

Responsibilities:

* Maintain customer identity across frames
* Reduce duplicate counting
* Support dwell-time calculations
* Provide trajectory information

---

# Re-Identification Layer

The ReID manager links observations of the same customer across different cameras.

Benefits:

* Reduces duplicate visitor counts
* Supports cross-camera customer journeys
* Enables accurate store-level analytics

---

# Staff Exclusion

Staff members can repeatedly appear throughout the day and distort analytics.

The system excludes staff using:

* Persistent presence duration
* Frequent reappearance patterns
* Dedicated staff detection logic

Benefits:

* Improved visitor counts
* More accurate dwell-time metrics
* Better conversion analytics

---

# Zone Analytics

Zones are configured for important store areas.

Examples:

* Entrance
* Billing Area
* Product Display Area
* Promotional Zone

Generated events:

* zone_enter
* zone_exit
* zone_dwell

---

# Entry / Exit Analytics

Virtual counting lines are configured near store entrances.

Generated events:

* entry
* exit

These events drive footfall analytics.

---

# Event Generation

All analytics are converted into structured JSONL events.

Example event types:

* entry
* exit
* zone_enter
* zone_exit
* zone_dwell
* anomaly

Events are written to:

sample_events.jsonl

and

events.jsonl

for downstream analytics.

---

# Analytics API

FastAPI exposes analytics endpoints.

Available endpoints:

* /health
* /events/ingest
* /stores/{store_id}/metrics
* /stores/{store_id}/heatmap
* /stores/{store_id}/funnel
* /stores/{store_id}/anomalies

The API layer aggregates event data into business metrics.

---

# Dashboard

The Streamlit dashboard provides:

* Store-level analytics
* Camera-wise analytics
* Event distribution
* Customer funnel
* Zone popularity
* Heatmap visualizations
* Anomaly monitoring

---

# Data Storage

SQLite is used for lightweight analytics storage.

Stored information:

* Aggregated metrics
* Event summaries
* Heatmap statistics

---

# Scalability Considerations

The architecture is intentionally modular.

Future enhancements:

* PostgreSQL backend
* Kafka event streaming
* Distributed camera processing
* GPU inference servers
* Cloud-native deployment

---

# AI-Assisted Decisions

AI tools were used as engineering assistants for:

* Reviewing architecture options
* Comparing deployment approaches
* Improving documentation quality
* Evaluating alternative API structures

All final design decisions, implementation, testing, and validation were performed manually by the project author.

The submitted solution reflects independently verified engineering decisions.
