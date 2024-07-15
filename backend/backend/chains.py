"""Module for the chains."""

import os

from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_community.utilities import SQLDatabase
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_community.tools import QuerySQLDataBaseTool

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
    model = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key=os.getenv("OPENAI_SECRET"))

    def clean(query: str) -> str:
        return query.replace(";", "")

    execute_query = QuerySQLDataBaseTool(db=db)
    write_query = create_sql_query_chain(model, db)

    chain = write_query | clean | execute_query
    result = chain.invoke(
        {
            "question": "Provide me a list of 5 campsites who are an ocffmember and have atleast 4 stars. Order by stars desc. Include name, adress and website."
        }
    )

    return result
