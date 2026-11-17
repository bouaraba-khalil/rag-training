import os
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from dotenv import load_dotenv

load_dotenv()

os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")


llm = init_chat_model("cohere:command-a-03-2025", temperature=0)

wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=800))


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

agent = create_agent(model=llm, tools=[wiki], system_prompt=SYSTEM_PROMPT)

question = "Who created the Python programming language and in which year was it first released?"
result = agent.invoke({"messages": [{"role": "user", "content": question}]})
print_trace(result)
