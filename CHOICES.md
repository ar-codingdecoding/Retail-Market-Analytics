# CHOICES.md

## Overview

This document explains the key technical choices made while building the Store Intelligence system. The objective of the project is to convert CCTV footage into structured retail analytics that can be consumed through APIs and dashboards.

---

## 1. Model Selection

The detection pipeline uses YOLO11s as the primary object detection model.

### Why YOLO11s

Several factors influenced this decision:

* Real-time inference capability.
* Good balance between speed and accuracy.
* Strong performance on person detection tasks.
* Easy integration with OpenCV-based video processing pipelines.
* Availability of pretrained weights, reducing training requirements.

The challenge focused on analytics generation rather than model training. Therefore, a pretrained detector was selected to prioritize reliability and development speed.

### Alternatives Considered

* YOLO11n: Faster but lower detection accuracy.
* YOLO11m: Higher accuracy but increased computational cost.
* Faster R-CNN: Accurate but unsuitable for near real-time processing.

YOLO11s provided the best trade-off for this implementation.

---

## 2. Event Schema Design

The analytics system converts visual observations into structured events.

Each event contains:

* event_type
* store_id
* camera_id
* visitor_id
* timestamp

Example event types:

* ENTRY
* EXIT
* RE_ENTRY
* ZONE_ENTER
* ZONE_DWELL
* BILLING_QUEUE_JOIN

### Why Event-Based Architecture

Instead of directly storing metrics, raw events are stored first.

Advantages:

* Metrics can be recomputed later.
* Historical analytics remain available.
* New KPIs can be created without reprocessing videos.
* Easier debugging and auditing.

This design follows common event-stream processing patterns used in production analytics systems.

---

## 3. API Design Decision

The API was designed around store-level analytics endpoints.

Examples:

* GET /stores/{store_id}/metrics
* GET /stores/{store_id}/funnel
* GET /stores/{store_id}/heatmap
* GET /stores/{store_id}/anomalies
* POST /events/ingest

### Reasoning

The problem statement focuses on retail-store intelligence rather than individual camera feeds.

Store-centric endpoints provide:

* Simpler dashboard integration.
* Easier aggregation across cameras.
* Reduced client-side processing.
* Clear separation between ingestion and analytics layers.

The ingestion endpoint remains independent so that analytics can be generated from any detection pipeline producing compatible events.

---

## Conclusion

The final architecture prioritizes simplicity, maintainability, and extensibility. The selected detector, event schema, and API structure together provide a practical foundation for retail intelligence analytics while remaining easy to deploy and evaluate.

# CHOICES.md

## Overview

This document explains the key technical choices made while building the Store Intelligence system. The objective of the project is to convert CCTV footage into structured retail analytics that can be consumed through APIs and dashboards.

---

## 1. Model Selection

The detection pipeline uses YOLO11s as the primary object detection model.

### Why YOLO11s

Several factors influenced this decision:

* Real-time inference capability.
* Good balance between speed and accuracy.
* Strong performance on person detection tasks.
* Easy integration with OpenCV-based video processing pipelines.
* Availability of pretrained weights, reducing training requirements.

The challenge focused on analytics generation rather than model training. Therefore, a pretrained detector was selected to prioritize reliability and development speed.

### Alternatives Considered

* YOLO11n: Faster but lower detection accuracy.
* YOLO11m: Higher accuracy but increased computational cost.
* Faster R-CNN: Accurate but unsuitable for near real-time processing.

YOLO11s provided the best trade-off for this implementation.

---

## 2. Event Schema Design

The analytics system converts visual observations into structured events.

Each event contains:

* event_type
* store_id
* camera_id
* visitor_id
* timestamp

Example event types:

* ENTRY
* EXIT
* RE_ENTRY
* ZONE_ENTER
* ZONE_DWELL
* BILLING_QUEUE_JOIN

### Why Event-Based Architecture

Instead of directly storing metrics, raw events are stored first.

Advantages:

* Metrics can be recomputed later.
* Historical analytics remain available.
* New KPIs can be created without reprocessing videos.
* Easier debugging and auditing.

This design follows common event-stream processing patterns used in production analytics systems.

---

## 3. API Design Decision

The API was designed around store-level analytics endpoints.

Examples:

* GET /stores/{store_id}/metrics
* GET /stores/{store_id}/funnel
* GET /stores/{store_id}/heatmap
* GET /stores/{store_id}/anomalies
* POST /events/ingest

### Reasoning

The problem statement focuses on retail-store intelligence rather than individual camera feeds.

Store-centric endpoints provide:

* Simpler dashboard integration.
* Easier aggregation across cameras.
* Reduced client-side processing.
* Clear separation between ingestion and analytics layers.

The ingestion endpoint remains independent so that analytics can be generated from any detection pipeline producing compatible events.

---

## Conclusion

The final architecture prioritizes simplicity, maintainability, and extensibility. The selected detector, event schema, and API structure together provide a practical foundation for retail intelligence analytics while remaining easy to deploy and evaluate.
