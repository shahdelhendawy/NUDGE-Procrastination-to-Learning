sessions: dict = {}

def create_session(session_id: str, goal: str, level: str, available_time: int, task):
    sessions[session_id] = {
        "goal": goal,
        "level": level,
        "available_time": available_time,
        "current_task": task,
        "history": [],
        "skip_streak": 0,
    }

def get_session(session_id: str):
    return sessions.get(session_id)