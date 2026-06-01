# DESIGN.md

# Store Intelligence System – Architecture Design

## Overview

This project implements an AI-powered Store Intelligence System that processes CCTV footage, detects and tracks customers, generates behavioral events, ingests those events into a real-time analytics API, and exposes operational intelligence through dashboards and REST endpoints.

The system is designed around an event-driven architecture where computer vision acts as the source of truth and all analytics are derived from emitted behavioral events.

---

# High-Level Architecture

```text
CCTV Footage
      │
      ▼
YOLO11 Person Detection
      │
      ▼
ByteTrack Multi-Object Tracking
      │
      ▼
Zone Classification
      │
      ▼
Event Generation
(ZONE_ENTER, ZONE_EXIT, ZONE_DWELL)
      │
      ▼
events.jsonl
      │
      ▼
FastAPI Ingestion Layer
      │
      ▼
SQLite Event Store
      │
      ▼
Analytics Engine
      │
      ├── Metrics
      ├── Funnel
      ├── Heatmap
      └── Anomalies
      │
      ▼
Dashboard / REST APIs
```

---

# Detection Pipeline

## Person Detection

The detection layer uses YOLO11s.

Reasons:

* Fast inference speed
* Strong person detection accuracy
* Minimal configuration
* Works effectively on retail CCTV footage

Only the person class is processed.

Non-person objects are ignored.

---

## Tracking

ByteTrack is used for multi-object tracking.

Each detected customer receives a stable track ID.

Tracking allows:

* Visitor counting
* Dwell calculation
* Zone transitions
* Session generation

Without tracking, every frame would be treated as a new visitor.

---

## Zone Classification

Store areas are represented as manually defined polygons/rectangles.

Example:

* DISPLAY
* MAKEUP

Each tracked visitor is assigned to a zone using the center point of the bounding box.

---

## Event Generation

The system emits structured behavioral events.

Current events:

### ZONE_ENTER

Generated when a visitor enters a zone.

### ZONE_EXIT

Generated when a visitor leaves a zone.

### ZONE_DWELL

Generated when a visitor remains in a zone for a configurable duration.

---

# Event Schema

Each event contains:

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

Properties:

* event_id → globally unique
* visitor_id → tracked customer
* event_type → behavioral action
* camera_id → source camera
* zone → store section
* confidence → event confidence
* timestamp → UTC timestamp

---

# Event Storage

Events are persisted into SQLite.

Benefits:

* Lightweight
* Easy deployment
* No external dependencies
* Sufficient for challenge-scale workloads

Table:

events

Columns:

* event_id
* visitor_id
* event_type
* camera_id
* zone
* confidence
* timestamp

---

# Analytics Layer

Analytics are computed from stored events.

## Metrics

Provides:

* Total events
* Zone entries
* Dwell events

---

## Funnel

Computes:

```text
ZONE_ENTER
     ↓
ZONE_DWELL
```

and calculates engagement rate.

---

## Heatmap

Computes:

* Zone popularity
* Relative zone usage

Heatmap values are normalized to 0–100.

A data_confidence flag is exposed when visitor counts are low.

---

## Anomaly Detection

Current anomaly:

### DEAD_ZONE

Triggered when no visitor activity exists for the requested store.

Severity levels:

* INFO
* WARN
* CRITICAL

can be extended in future versions.

---

# Dashboard

A Streamlit dashboard visualizes:

* Metrics
* Funnel
* Zone popularity
* Heatmaps
* Anomalies

The dashboard consumes the FastAPI endpoints directly.

---

# AI-Assisted Decisions

The project was developed with AI assistance for:

* Architecture brainstorming
* Event schema design
* Analytics API design
* Detection pipeline refinement
* Documentation generation

All generated suggestions were reviewed and modified before implementation.

---

# Trade-Offs

## Re-Identification

A full production-grade ReID model was not implemented due to limited footage and absence of labeled identity data.

A lightweight prototype was evaluated.

---

## Staff Detection

Multiple approaches were considered:

* Fixed region filtering
* Uniform color detection

Due to customer movement across all zones and lack of dedicated staff labels, automatic staff exclusion was documented as a limitation rather than forcing inaccurate classifications.

---

# Future Improvements

* DeepSORT / StrongSORT integration
* Person Re-Identification embeddings
* POS transaction correlation
* Billing queue analytics
* Multi-camera visitor stitching
* Kafka-based event streaming
* PostgreSQL migration
* Real-time WebSocket dashboard

---

# Conclusion

The final system demonstrates an end-to-end AI-powered Store Intelligence platform capable of transforming raw CCTV footage into actionable retail analytics through detection, tracking, event generation, analytics APIs, anomaly detection, and live dashboards.
