from fastapi import FastAPI
from app.models.learning import StartRequest, StartResponse
from app.services.ai_service import generate_first_task
import uuid

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/start", response_model=StartResponse)
def start_session(request: StartRequest):
    task = generate_first_task(
        goal=request.goal,
        level=request.level,
        available_time=request.available_time,
    )

    return StartResponse(
        session_id=str(uuid.uuid4()),
        tasks=[task],
    )