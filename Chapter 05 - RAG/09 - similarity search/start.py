import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_cohere import CohereEmbeddings

load_dotenv()

os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")


CHAPTER_DIR = Path(__file__).resolve().parents[1]
PERSIST_DIR = str(CHAPTER_DIR / "chroma_db")


def get_embeddings():
    return CohereEmbeddings(model="embed-english-v3.0")


def get_vectorstore():
    return Chroma(
        collection_name="corpus",
        embedding_function=get_embeddings(),
        persist_directory=PERSIST_DIR,
    )


vs = get_vectorstore()
print("chunks in store:", vs._collection.count())
