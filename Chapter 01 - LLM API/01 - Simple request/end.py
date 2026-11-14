import cohere
import os

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("COHERE_API_KEY")

client = cohere.ClientV2(api_key)

response = client.chat(
    model="command-a-03-2025",
    messages=[
        {
            "role": "user",
            "content": "How many wilayas are there in Algeria?",
        }
    ],
    max_tokens=1000,
)

print(f"User: How many wilayas are there in Algeria?\n\n")

for block in response.message.content:
    if block.type == "text":
        print(f"Cohere: {block.text}")