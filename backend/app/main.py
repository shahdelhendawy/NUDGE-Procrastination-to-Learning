from fastapi import FastAPI
from app.models.learning import StartRequest, StartResponse, Task

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/start", response_model=StartResponse)
def start_session(request: StartRequest):
    return StartResponse(
        session_id="test-session-1",
        tasks=[
            Task(
                id="task_1",
                title="Placeholder task",
                description=f"A tiny first step for: {request.goal}",
                type="read",
                estimated_minutes=3,
                difficulty="easy"
            )
        ]
    )