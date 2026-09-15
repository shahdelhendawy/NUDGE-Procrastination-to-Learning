from google import genai
from google.genai import types
from app.core.config import GEMINI_API_KEY
from app.models.learning import Task

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