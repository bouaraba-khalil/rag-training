import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")


llm = init_chat_model("cohere:command-a-03-2025")

parser = StrOutputParser()

template = ChatPromptTemplate.from_messages([
    ("system", "You are a summarizer. You will summarize the following text."),
    ("human", "{text}"),
])


while True: 
    user_input = input("Enter your text to summarize: ")
    if user_input.lower() == "exit":
        break

    chain = template | llm | parser
    response = chain.invoke({
        "text": user_input
    })
    print(f"Summarized text: {response}")
    print(f"\n\n")
