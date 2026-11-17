import os
from typing import Literal
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")


llm = init_chat_model("cohere:command-a-03-2025", temperature=0)


class Question(BaseModel):
    question: str
    answer: str
    difficulty: Literal["easy", "medium", "hard"]


class Quiz(BaseModel):
    questions: list[Question]


summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a summarizer. You will summarize the following text."),
    ("human", "{text}"),
])
summary_chain = summary_prompt | llm | StrOutputParser()

questions_prompt = ChatPromptTemplate.from_messages([
    ("system", "You write short-answer quiz questions strictly from the provided text."),
    ("human", "Write exactly {n} questions based only on this summary.\n\n{summary}"),
])
questions_chain = questions_prompt | llm.with_structured_output(Quiz)


while True: 
    user_input = input("Enter your text: ")
    if user_input.lower() == "exit":
        break

    n = input("How many questions? ")

    summary = summary_chain.invoke({"text": user_input})
    quiz = questions_chain.invoke({"summary": summary, "n": n})

    print(f"Summary: {summary}")
    for question in quiz.questions:
        print(f"[{question.difficulty}] {question.question} -> {question.answer}")
    print(f"\n\n")
