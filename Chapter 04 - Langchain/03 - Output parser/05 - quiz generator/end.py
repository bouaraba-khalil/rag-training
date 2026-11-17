import os
from typing import Literal
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")


llm = init_chat_model("cohere:command-a-03-2025", temperature=0)


class Question(BaseModel):
    question: str
    answer: str
    difficulty: Literal["easy", "medium", "hard"]


class Quiz(BaseModel):
    questions: list[Question]


template = ChatPromptTemplate.from_messages([
    ("system", "You write short-answer quiz questions strictly from the provided text."),
    ("human", "Write exactly {n} questions based only on the text below.\n\n{text}"),
])


while True: 
    user_input = input("Enter your text: ")
    if user_input.lower() == "exit":
        break

    n = input("How many questions? ")

    chain = template | llm.with_structured_output(Quiz)
    quiz = chain.invoke({
        "n": n,
        "text": user_input
    })

    for question in quiz.questions:
        print(f"[{question.difficulty}] {question.question} -> {question.answer}")
    print(f"\n\n")
