# CHOICES.md

# Engineering Decisions

This document explains the major engineering decisions made during the development of the Store Intelligence System.

---

# Decision 1: Detection Model Selection

## Chosen

YOLO11s

## Alternatives Considered

### YOLO11n

Pros:

* Faster inference
* Lower resource usage

Cons:

* Lower detection accuracy
* Missed smaller customers in crowded scenes

### YOLO11m

Pros:

* Higher accuracy

Cons:

* Slower inference
* Higher hardware requirements

## Why YOLO11s Was Chosen

YOLO11s provided the best balance between:

* Accuracy
* Speed
* Simplicity

The retail CCTV footage contained multiple people with varying scales and partial occlusions. YOLO11s maintained stable detection quality while remaining suitable for real-time processing.

---

# Decision 2: Tracking Architecture

## Chosen

ByteTrack

## Alternatives Considered

### DeepSORT

Pros:

* Appearance embeddings
* Better re-identification

Cons:

* More complex
* Additional model dependencies

### StrongSORT

Pros:

* Strong identity preservation

Cons:

* Higher computational cost

## Why ByteTrack Was Chosen

ByteTrack offers:

* Simple integration
* Real-time performance
* Stable tracking IDs

For the provided CCTV clips, ByteTrack generated sufficiently stable visitor identities while keeping implementation complexity low.

---

# Decision 3: API Architecture

## Chosen

FastAPI + SQLite

## Alternatives Considered

### Flask

Pros:

* Simple

Cons:

* No automatic OpenAPI generation
* Less structured validation

### PostgreSQL

Pros:

* Production ready
* Better scalability

Cons:

* Additional setup complexity

## Why FastAPI Was Chosen

FastAPI provides:

* Automatic Swagger documentation
* Type validation
* High performance
* Clean API development experience

The challenge explicitly required production-style APIs, making FastAPI a strong choice.

## Why SQLite Was Chosen

SQLite provides:

* Zero configuration
* Single-file deployment
* Easy local development

Given the limited dataset size and challenge timeline, SQLite was sufficient.

---

# Event Schema Design Decision

The event schema was intentionally designed around behavioral events rather than raw detections.

Example:

```json
{
  "event_type": "ZONE_ENTER",
  "visitor_id": "5",
  "camera_id": "CAM2",
  "zone": "DISPLAY"
}
```

Advantages:

* Easier analytics
* Decoupled architecture
* Smaller storage footprint
* Extensible event catalog

---

# AI Usage

AI tools were used extensively throughout development.

Examples:

* Architecture planning
* Event schema design
* Analytics API design
* Detection pipeline debugging
* Documentation generation

All outputs were reviewed, tested, and modified before inclusion in the final implementation.

---

# Decisions Rejected

## Full Re-Identification Model

Considered:

* OSNet
* TorchReID

Rejected because:

* No labeled identity dataset
* Limited challenge footage
* Additional complexity

A lightweight prototype was explored instead.

---

## Staff Classification

Considered:

* Uniform color classification
* Fixed-area exclusion

Rejected as a mandatory production feature because customer movement patterns overlapped heavily with potential staff locations, producing unreliable classifications on the available footage.

The limitation is documented for future improvement.

---

# Conclusion

The selected architecture prioritized reliability, simplicity, explainability, and challenge completion while maintaining a clear path toward production-scale expansion.
