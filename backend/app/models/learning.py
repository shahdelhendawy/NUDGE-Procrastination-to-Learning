from typing import List, Literal
from pydantic import BaseModel

class StartRequest(BaseModel):
    goal: str
    level: str
    available_time: int

class Task(BaseModel):
    id: str
    title: str
    description: str
    type: str
    estimated_minutes: int
    difficulty: Literal["easy", "medium", "hard"]

class TaskWithFeedback(BaseModel):
    task: Task
    feedback: str | None = None

class StartResponse(BaseModel):
    session_id: str
    tasks: List[Task]

class AnswerRequest(BaseModel):
    task_id: str
    status: Literal["completed", "skipped", "wrong"]
    answer: str | None = None

class AnswerResponse(BaseModel):
    session_id: str
    next_task: Task
    feedback: str | None = None