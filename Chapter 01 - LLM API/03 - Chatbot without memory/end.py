import cohere
import os

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("COHERE_API_KEY")

client = cohere.ClientV2(api_key)
while True:
    question = input("You: ")
    if question.lower() in ["exit", "quit"]:
        break
    print(f"\n")
    response = client.chat(
        model="command-a-03-2025",
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        max_tokens=1000,
    )


    for block in response.message.content:
        if block.type == "text":
            print(f"Cohere: {block.text}")

    print(f"\n\n")
