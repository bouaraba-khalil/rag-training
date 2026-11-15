import cohere
import os

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("COHERE_API_KEY")

client = cohere.ClientV2(api_key)
context = input("Context: ")
question = input("Question: ")
print(f"\n\n")
response = client.chat(
    model="command-a-03-2025",
    messages=[
        {
            "role": "system",
            "content": "Answer the user's question using only the context they provide. If the answer is not in the context, say you don't know.",
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}",
        }
    ],
    max_tokens=1000,
)


for block in response.message.content:
    if block.type == "text":
        print(f"Cohere: {block.text}")
