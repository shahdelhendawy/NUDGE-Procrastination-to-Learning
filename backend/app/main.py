from fastapi import FastAPI, HTTPException
from app.models.learning import StartRequest, StartResponse, AnswerRequest, AnswerResponse
from app.services.ai_service import generate_first_task, generate_next_task
from app.services.session_store import create_session, get_session
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

    session_id = str(uuid.uuid4())

    create_session(
        session_id=session_id,
        goal=request.goal,
        level=request.level,
        available_time=request.available_time,
        task=task,
    )

    return StartResponse(
        session_id=session_id,
        tasks=[task],
    )

@app.post("/sessions/{session_id}/answer", response_model=AnswerResponse)
def answer_task(session_id: str, request: AnswerRequest):
    session = get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    previous_task = session["current_task"]

    if request.status == "skipped":
        session["skip_streak"] += 1
    else:
        session["skip_streak"] = 0

    force_start_now = session["skip_streak"] >= 2

    next_task, feedback = generate_next_task(
        goal=session["goal"],
        level=session["level"],
        previous_task=previous_task,
        status=request.status,
        force_start_now=force_start_now,
    )

    session["history"].append({
        "task_id": request.task_id,
        "status": request.status,
    })
    session["current_task"] = next_task

    return AnswerResponse(
        session_id=session_id,
        next_task=next_task,
        feedback=feedback,
    )