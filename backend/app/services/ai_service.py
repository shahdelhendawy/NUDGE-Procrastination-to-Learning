from google import genai
from google.genai import types
from app.core.config import GEMINI_API_KEY
from app.models.learning import Task, TaskWithFeedback

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_first_task(goal: str, level: str, available_time: int) -> Task:
    prompt = f"""
    A student wants to learn: "{goal}"
    Their level is: {level}
    They have {available_time} minutes available right now.

    Do NOT create a big study plan.
    Create ONE tiny, extremely easy-to-start task that takes about 2-5 minutes,
    to reduce the friction of starting.

    The "difficulty" field must reflect how hard THIS SPECIFIC TASK is
    (usually "easy", since it should be a very small first step),
    NOT the student's overall level.
    """

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Task,
        ),
    )

    return Task.model_validate_json(response.text)

def generate_next_task(goal: str, level: str, previous_task, status: str, force_start_now: bool = False) -> tuple[Task, str | None]:
    if force_start_now:
        instruction = """
        The student has SKIPPED multiple tasks in a row and seems unable to start at all.
        Activate "Start Now mode": create an EXTREMELY tiny task (5-15 seconds),
        almost trivially easy, just to get them to take any first action
        (e.g. opening the editor and typing one single word or line).
        Do not worry about teaching anything meaningful yet — the only goal is starting.
        """
    elif status == "completed":
        instruction = """
        The student COMPLETED the previous task successfully.
        Create the next task as a logical next step, slightly more challenging.
        """
    elif status == "wrong":
        instruction = """
        The student got the previous task WRONG or misunderstood it.
        First, briefly explain the correct idea in 1-2 simple sentences,
        then create an EASIER task focusing on the same basic idea.
        """
    else:  # skipped
        instruction = """
        The student SKIPPED the previous task (could not start it).
        Create a MUCH SMALLER and easier task (30 seconds to 2 minutes),
        to reduce the starting friction as much as possible.
        """

    prompt = f"""
    A student's overall learning goal is: "{goal}"
    Their level is: {level}
    Their previous task was: "{previous_task.title}" - {previous_task.description}

    {instruction}

    Do NOT create a big study plan. Create ONE tiny task only.
    The "difficulty" field must reflect how hard THIS SPECIFIC TASK is,
    NOT the student's overall level.
    """

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=TaskWithFeedback,
        ),
    )

    result = TaskWithFeedback.model_validate_json(response.text)
    return result.task, result.feedback