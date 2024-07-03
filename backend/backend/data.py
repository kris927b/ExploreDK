"""Module containing data models for AI output"""

from langchain_core.pydantic_v1 import BaseModel, Field


class Question(BaseModel):
    """Data model for individual answers."""

    idx: int = Field("Integer ID of the question. Should be between 1 and 50.")
    question_text: str = Field("Question for the user. Should be max 1 sentence.")
    possible_answers: list[str] = Field(
        "List of possible answers for the users to select from. "
        "There should be between 2 to 5 possible answers."
    )
    answers_allowed: int = Field(
        "Number of the answers the user can maximally select. Should be minimum 1."
    )


class QuestionList(BaseModel):
    """Data model for a group of questions."""

    idx: int = Field("Integer ID of the question group. Should be between 1 and 100")
    question_1: Question = Field("The first question for the user.")
    question_2: Question = Field("The second question for the user.")
    question_3: Question = Field("The third question for the user.")
    question_4: Question = Field("The fourth question for the user.")
    question_5: Question = Field("The fifth question for the user.")
