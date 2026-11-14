import cohere
import os

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("COHERE_API_KEY")
messages = []
client = cohere.ClientV2(api_key)
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
        "content": response.message.content,
    })


    for block in response.message.content:
        if block.type == "text":
            print(f"Cohere: {block.text}")

    print(f"\n\n")

for block in messages:
    print(f"{block['role']}: {block['content'] if isinstance(block['content'], str) else block['content'][0].text}\n")