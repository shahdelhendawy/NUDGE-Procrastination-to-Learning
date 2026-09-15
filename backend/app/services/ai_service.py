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

def generate_concept(goal: str, level: str, previous_concept: str | None = None) -> Task:
    if previous_concept:
        context = f'The student just mastered the concept: "{previous_concept}". Now explain the next logical concept that builds on it.'
    else:
        context = "This is the very first concept for this goal. Pick the most fundamental starting concept."

    research_prompt = f"""
    A student's learning goal is: "{goal}"
    Their level is: {level}

    {context}

    Explain this ONE concept in a very short, simple way (3-5 lines max),
    with a small concrete example. Do not write a full lesson.

    Also search and find ONE real, trustworthy resource (article, documentation,
    or tutorial page) where the student can read more about this exact concept.
    """

    research_response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=research_prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
        ),
    )

    structuring_prompt = f"""
    Convert the following explanation into the required task format.
    Set "type" to "concept". Extract the real resource URL you find in the text
    into "resource_url", and a short label for it into "resource_label".

    Explanation text:
    {research_response.text}
    """

    structured_response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=structuring_prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Task,
        ),
    )

    return Task.model_validate_json(structured_response.text)