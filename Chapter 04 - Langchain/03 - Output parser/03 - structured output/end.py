import os
from typing import Literal
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")


llm = init_chat_model("cohere:command-a-03-2025", temperature=0)


class Summary(BaseModel):
    title: str = Field(description="A short title, 8 words maximum")
    key_points: list[str] = Field(description="Between 3 and 5 key points")
    sentiment: Literal["positive", "neutral", "negative"] = Field(description="Overall tone of the text")


template = ChatPromptTemplate.from_messages([
    ("system", "Extract a structured summary of the text."),
    ("human", "{text}"),
])


while True: 
    user_input = input("Enter your text to summarize: ")
    if user_input.lower() == "exit":
        break

    chain = template | llm.with_structured_output(Summary)
    result = chain.invoke({
        "text": user_input
    })
    print(type(result).__name__)
    print(f"Title: {result.title}")
    print(f"Sentiment: {result.sentiment}")
    print(f"Key points: {result.key_points}")
    print(f"\n\n")
