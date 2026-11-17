import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")


llm = init_chat_model("cohere:command-a-03-2025")

lang_input = input("Enter the language you want to translate to: ")


template = ChatPromptTemplate.from_messages([
    ("system", f"You are a translator. You will translate the following text to {lang_input}."),
    ("human", "{text}"),
])


while True: 
    user_input = input("Enter your text to translate: ")
    if user_input.lower() == "exit":
        break

    chain = template | llm
    response = chain.invoke({
        "text": user_input
    })
    print(f"Translated text: {response.content}")
    print(f"\n\n")
