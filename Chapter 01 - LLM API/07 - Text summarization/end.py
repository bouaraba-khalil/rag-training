import cohere
import os

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("COHERE_API_KEY")

client = cohere.ClientV2(api_key)
text = input("Text: ")
print(f"\n\n")
response = client.chat(
    model="command-a-03-2025",
    messages=[
        {
            "role": "system",
            "content": "Summarize the user's text in two sentences.",
        },
        {
            "role": "user",
            "content": text,
        }
    ],
    max_tokens=1000,
)


for block in response.message.content:
    if block.type == "text":
        print(f"Cohere: {block.text}")
