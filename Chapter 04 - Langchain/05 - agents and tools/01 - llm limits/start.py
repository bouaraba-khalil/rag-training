import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")


llm = init_chat_model("cohere:command-a-03-2025", temperature=0)

question = "What is 48271 * 9183? And what is today's date?"

answer = llm.invoke(question)
print("LLM says:", answer.content)
