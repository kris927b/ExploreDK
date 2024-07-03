"""Module for the chains."""

import os

from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_community.utilities import SQLDatabase
from langchain.chains.sql_database.query import create_sql_query_chain

from langchain_openai import ChatOpenAI

from backend.prompts import QUESTION_PROMPT
from backend.data import QuestionList


def generate_questions() -> QuestionList:
    """Generate the questions to serve the user

    Returns:
        QuestionList: List of questions to serve.
    """
    question_parser = PydanticOutputParser(pydantic_object=QuestionList)

    model = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_SECRET"))

    prompt = PromptTemplate(
        template=QUESTION_PROMPT,
        input_variables=["response_template"],
    )

    chain = prompt | model | question_parser

    output = chain.invoke(
        {"response_template": question_parser.get_format_instructions()}
    )

    return output


def generate_recommendations():
    db = SQLDatabase.from_uri("sqlite:///database/campsites.db")

    return db.get_table_info()
