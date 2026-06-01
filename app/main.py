from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.models import Base
from app.database import engine

Base.metadata.create_all(bind=engine)

from app.services import (
    get_metrics,
    get_heatmap,
    get_funnel,
    get_anomalies,
    ingest_events
)

app = FastAPI(
    title="Store Intelligence API"
)


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/events/ingest")
async def ingest(request: Request):

    try:

        data = await request.json()

        return ingest_events(data)

    except Exception as e:

        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": str(e)
            }
        )


@app.get("/stores/{store_id}/metrics")
def metrics(store_id: str):

    return get_metrics(
        store_id
    )


@app.get("/stores/{store_id}/funnel")
def funnel(store_id: str):

    return get_funnel(
        store_id
    )


@app.get("/stores/{store_id}/heatmap")
def heatmap(store_id: str):

    return get_heatmap(
        store_id
    )


@app.get("/stores/{store_id}/anomalies")
def anomalies(store_id: str):

    return get_anomalies(
        store_id
    )