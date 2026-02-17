from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import uvicorn
from routers import members, foods, exercises, workouts, plans, exports

app = FastAPI(
    title="HealthAI Coach API",
    description="API REST backend pour la plateforme HealthAI Coach",
    version="1.0.0",
)

app.include_router(members.router)
app.include_router(foods.router)
app.include_router(exercises.router)
app.include_router(workouts.router)
app.include_router(plans.router)
app.include_router(exports.router)


@app.get("/", tags=["Health"])
def read_root():
    return {"message": "HealthAI Coach API is running", "docs": "/docs"}


@app.get("/metrics", tags=["Monitoring"])
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
