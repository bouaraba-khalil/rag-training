import cohere
import os

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("COHERE_API_KEY")

client = cohere.ClientV2(api_key)
language = input("Language: ")
text = input("Text: ")
print(f"\n\n")
response = client.chat(
    model="command-a-03-2025",
    messages=[
        {
            "role": "system",
            "content": "Translate the user's text into the language they request. Return only the translation.",
        },
        {
            "role": "user",
            "content": f"Language: {language}\n\nText:\n{text}",
        }
    ],
    max_tokens=1000,
)


for block in response.message.content:
    if block.type == "text":
        print(f"Cohere: {block.text}")
