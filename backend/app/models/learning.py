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

class StartResponse(BaseModel):
    session_id: str
    tasks: List[Task]