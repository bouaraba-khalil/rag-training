import os
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")


llm = init_chat_model("cohere:command-a-03-2025", temperature=0)


@tool
def get_weather(city: str) -> str:
    """Return the current weather for a city. Use this whenever the user asks about the weather."""
    return f"It is actually 20 degrees in {city} and it is actually sunny."


def print_trace(result):
    """Print an agent run: human message, tool calls, tool results, final answer."""
    for message in result["messages"]:
        if message.type == "human":
            print("HUMAN:", message.text)
        elif message.type == "ai" and message.tool_calls:
            for call in message.tool_calls:
                print("AI -> TOOL CALL:", call["name"], call["args"])
        elif message.type == "ai":
            print("AI (final):", message.text)
        elif message.type == "tool":
            print("TOOL RESULT:", message.text[:150].replace("\n", " "))


SYSTEM_PROMPT = (
    "You are a helpful assistant. Use your tools to look things up or compute them instead of guessing. "
    "Answer concisely."
)

agent = create_agent(model=llm, tools=[get_weather], system_prompt=SYSTEM_PROMPT)

question = "What is the weather in Tokyo?"
result = agent.invoke({"messages": [{"role": "user", "content": question}]})
print_trace(result)
