import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("GEMINI API KEY LOADED:", bool(api_key))

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        timeout=30000
    )
)


def analyze_task(
    task_description: str,
    user_skills: list[dict] | None = None
):
    """
    Analyze a task against the user's saved skills.

    user_skills example:
    [
        {"skill": "Python", "level": 4},
        {"skill": "FastAPI", "level": 2},
        {"skill": "PostgreSQL", "level": 1}
    ]
    """

    if user_skills is None:
        user_skills = []

    print("SENDING REQUEST TO GEMINI...")

    try:
        prompt = f"""
You are a senior software developer and a mentor for beginner developers.

Analyze the following software development task and personalize
your guidance using the user's actual saved skills.

TASK:
{task_description}

USER'S SAVED SKILLS:
{json.dumps(user_skills, ensure_ascii=False)}

Proficiency scale:
1 = Beginner
2 = Basic
3 = Intermediate
4 = Advanced
5 = Expert

Your responsibilities:

1. Explain the task in simple, beginner-friendly words.
2. Identify the technical skills genuinely required for this task.
3. For each required skill, estimate the minimum proficiency level
   needed to complete the task.
4. Compare each required skill with the user's saved skill level.
5. If a required skill is missing from the user's profile, treat it
   as an unknown skill. Do not assume the user knows it.
6. If the user's level is below the required level, explain the gap.
7. If the user's level meets or exceeds the required level, do not
   report that skill as a gap.
8. Give a logical learning order based on the user's gaps.
9. Provide a practical checklist to complete before coding.
10. Never invent proficiency levels that the user has not supplied.

Return only valid JSON with exactly this structure:

{{
    "task_explanation": "Simple explanation of the task",
    "required_skills": [
        {{
            "skill": "FastAPI",
            "required_level": 4,
            "user_level": 2,
            "status": "needs_improvement"
        }}
    ],
    "skill_gaps": [
        {{
            "skill": "FastAPI",
            "user_level": 2,
            "required_level": 4,
            "what_to_learn": "Learn how FastAPI routes and request validation work"
        }}
    ],
    "learning_order": [
        "Learn the relevant FastAPI concepts first"
    ],
    "pre_coding_checklist": [
        "Understand the existing API structure"
    ]
}}

Rules:
- Return only JSON. Do not use Markdown.
- Do not provide implementation code.
- Keep explanations beginner-friendly and actionable.
- Include only skills relevant to the task.
- Use status "needs_improvement" when the known level is below
  the required level.
- Use status "meets_requirement" when the known level meets
  or exceeds the required level.
- Use status "not_in_profile" when the user has not saved that skill.
- For "not_in_profile", set user_level to null.
- Do not mark a skill as a gap merely because its name is absent
  from the profile; explain that its level is unknown.
- Keep required_skills and skill_gaps consistent with one another.
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        print("RESPONSE RECEIVED FROM GEMINI")

        result = json.loads(response.text)

        print("JSON PARSED SUCCESSFULLY")

        return result

    except Exception as e:
        print("GEMINI ERROR:")
        print(type(e).__name__)
        print(str(e))
        raise

