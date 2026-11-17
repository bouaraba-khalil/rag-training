import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")

llm = init_chat_model("cohere:command-a-03-2025")

response = llm.invoke([
    {"role": "system", "content": "you can only give short answers"},
    {"role": "user", "content": "How many wilayas are there in Algeria?"}
])

print(response.content)
