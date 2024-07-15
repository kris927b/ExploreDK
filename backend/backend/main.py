"""Module for the endpoints."""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from dotenv import load_dotenv

from backend.chains import generate_questions, generate_recommendations

app = FastAPI(title="ExploreDK")


@app.get("/")
async def redirect_root_to_docs():
    """Redirect to docs when accessing root

    Returns:
        RedirectResponse: Redirect to docs page
    """
    return RedirectResponse("/docs")


@app.get("/questions")
async def get_questions() -> dict:
    """Endpoint to generate questions to ask the user.

    Returns:
        dict: Dictionary of questions.
    """
    load_dotenv()

    questions = generate_questions()

    return questions.dict()


@app.get("/database")
async def get_database_info() -> str:
    load_dotenv()

    return generate_recommendations()
