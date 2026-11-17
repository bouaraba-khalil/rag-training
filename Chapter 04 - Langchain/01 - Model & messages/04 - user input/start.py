import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")


llm = init_chat_model("cohere:command-a-03-2025")

response = llm.invoke([
    SystemMessage(content="you can only give short answers"),
    HumanMessage(content="How many wilayas are there in Algeria?")
])

print(response.content)
