# CHOICES.md

# Engineering Decisions and Trade-Offs

## Model Selection

### Selected Model

YOLO11s

### Reasons

* Fast inference speed
* Good person detection accuracy
* Suitable for near real-time processing
* Lightweight deployment requirements
* Strong performance on retail CCTV footage

### Alternatives Considered

YOLO11n

Pros:

* Faster

Cons:

* Lower accuracy

YOLO11m

Pros:

* Higher accuracy

Cons:

* Higher latency and compute cost

Decision:

YOLO11s provided the best balance between speed and accuracy.

---

# Tracking Strategy

A tracking layer was selected to maintain customer identities across frames.

Benefits:

* Prevents duplicate counts
* Enables dwell-time measurement
* Supports customer journey analysis

Without tracking, each frame would generate independent detections, reducing analytics quality.

---

# Re-Identification Strategy

A dedicated ReID manager was included.

Purpose:

* Link customers across cameras
* Improve visitor counting accuracy
* Support store-level analytics

Trade-Off:

Additional processing complexity was accepted in exchange for improved analytics quality.

---

# Staff Exclusion Strategy

Staff exclusion was implemented because employees can heavily bias retail metrics.

Benefits:

* Accurate visitor counts
* Better dwell-time measurements
* More realistic conversion calculations

---

# Event Schema Design

JSONL was selected as the primary event format.

Reasons:

* Human readable
* Stream friendly
* Easy to validate
* Easy ingestion into databases
* Compatible with analytics pipelines

Each line represents a single independent event.

---

# Database Selection

SQLite was selected.

Reasons:

* Lightweight
* Zero configuration
* Fast local development
* Suitable for challenge scope

Alternative:

PostgreSQL

Pros:

* Better scalability

Cons:

* Additional deployment complexity

Decision:

SQLite was sufficient for challenge requirements.

---

# API Architecture

FastAPI was selected.

Reasons:

* Automatic OpenAPI generation
* Swagger UI support
* High performance
* Easy validation with Pydantic

Benefits for reviewers:

* Easy endpoint testing
* Self-documenting API
* Simple deployment

---

# Dashboard Technology

Streamlit was selected.

Reasons:

* Fast development cycle
* Interactive analytics support
* Simple deployment
* Strong visualization ecosystem

---

# Deployment Decisions

API Deployment:
Render

Dashboard Deployment:
Streamlit Community Cloud

Reasons:

* Public accessibility
* Minimal infrastructure management
* Easy reviewer access

---

# Event Processing Design

A modular pipeline architecture was selected.

Components:

* Detection
* Tracking
* ReID
* Staff Filtering
* Zone Analytics
* Event Generation

Benefits:

* Easier testing
* Easier maintenance
* Independent component upgrades

---

# Testing Approach

Testing focused on:

* Event generation correctness
* API endpoint validation
* JSONL format validation
* Tracking consistency
* Edge-case handling

---

# AI-Assisted Decisions

AI tools were used during development as engineering assistants for:

* Exploring alternative designs
* Reviewing architecture options
* Comparing deployment strategies
* Improving documentation clarity

AI tools were not used as autonomous decision makers.

All final implementation decisions, validation, debugging, testing, and engineering trade-offs were performed and verified manually by the project author.
