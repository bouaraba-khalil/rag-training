import json
import os
from urllib.parse import quote
from urllib.request import urlopen

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")


llm = init_chat_model("cohere:command-a-03-2025", temperature=0)


# Short labels for the weather codes Open-Meteo returns.
# https://open-meteo.com/en/docs
WEATHER_CODES = {
    0: "clear",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "foggy",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "drizzle",
    55: "heavy drizzle",
    61: "light rain",
    63: "rain",
    65: "heavy rain",
    71: "light snow",
    73: "snow",
    75: "heavy snow",
    80: "light rain showers",
    81: "rain showers",
    82: "heavy rain showers",
    95: "thunderstorm",
    96: "thunderstorm with hail",
    99: "thunderstorm with heavy hail",
}


def _get_json(url: str) -> dict:
    with urlopen(url, timeout=10) as response:
        return json.load(response)


@tool
def get_weather(city: str) -> str:
    """Return the current weather for a city. Use this whenever the user asks about the weather."""
    geo = _get_json(
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={quote(city)}&count=1&language=en&format=json"
    )
    places = geo.get("results") or []
    if not places:
        return f"I could not find a city named {city}."

    place = places[0]
    weather = _get_json(
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={place['latitude']}&longitude={place['longitude']}"
        "&current=temperature_2m,weather_code,wind_speed_10m"
    )
    current = weather["current"]
    condition = WEATHER_CODES.get(current["weather_code"], "unknown conditions")
    return (
        f"It is {current['temperature_2m']}°C and {condition} in {place['name']}, "
        f"with wind at {current['wind_speed_10m']} km/h."
    )


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
