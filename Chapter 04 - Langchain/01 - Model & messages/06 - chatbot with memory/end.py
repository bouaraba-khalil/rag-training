import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")


llm = init_chat_model("cohere:command-a-03-2025")

messages = []
while True: 
    content = input("Enter your question: ")
    if content.lower() == "exit":
        break

    messages.append(HumanMessage(content=content))
    response = llm.invoke(messages)
    messages.append(AIMessage(content=response.content))

    print(response.content)
    print(f"\n\n")
