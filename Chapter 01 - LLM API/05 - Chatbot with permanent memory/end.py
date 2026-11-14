import cohere
import os
import json
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("COHERE_API_KEY")
messages = []
client = cohere.ClientV2(api_key)

try:
    with open("memory.json", "r") as f:
        messages = json.load(f)
except FileNotFoundError:
    pass


while True:
    question = input("You: ")
    if question.lower() in ["exit", "quit"]:
        print(f"\n\n")
        break
    
    print(f"\n")
    messages.append({
        "role": "user",
        "content": question,
    })

    response = client.chat(
        model="command-a-03-2025",
        messages=messages,
        max_tokens=1000,
    )
    messages.append({
        "role": "assistant",
        "content": response.message.content[0].text,
    })


    for block in response.message.content:
        if block.type == "text":
            print(f"Cohere: {block.text}")

    print(f"\n\n")

with open("memory.json", "w") as f:
    json.dump(messages, f)