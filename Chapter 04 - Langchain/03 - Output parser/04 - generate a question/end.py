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


template = ChatPromptTemplate.from_messages([
    ("system", "You write short-answer quiz questions strictly from the provided text."),
    ("human", "Write a questions based only on the text below.\n\n{text}"),
])


while True: 
    user_input = input("Enter your text: ")
    if user_input.lower() == "exit":
        break

    chain = template | llm.with_structured_output(Question)
    quiz = chain.invoke({
        "text": user_input
    })

    print(f"[{quiz.difficulty}] {quiz.question} -> {quiz.answer}")
    print(f"\n\n")
