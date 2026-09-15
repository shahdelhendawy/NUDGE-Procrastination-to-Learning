from typing import List
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
    difficulty: str

class StartResponse(BaseModel):
    session_id: str
    tasks: List[Task]