import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")


llm = init_chat_model("cohere:command-a-03-2025")

template = ChatPromptTemplate.from_messages([
    ("system", "You are a translator. You will translate the following text from French to English."),
    ("human", "{text}"),
])


user_input = input("Enter your text to translate: ")

chain = template | llm

response = chain.invoke({
    "text": user_input
})

print(f"Translated text: {response.content}")
