import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_cohere import CohereEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")


CHAPTER_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = CHAPTER_DIR / "data"
PERSIST_DIR = str(CHAPTER_DIR / "chroma_db")


def get_embeddings():
    return CohereEmbeddings(model="embed-english-v3.0")


def get_vectorstore():
    return Chroma(
        collection_name="corpus",
        embedding_function=get_embeddings(),
        persist_directory=PERSIST_DIR,
    )


def load_corpus():
    docs = []
    for path in sorted(DATA_DIR.glob("*.pdf")):
        for d in PyPDFLoader(str(path)).load():
            d.metadata["doc_type"] = "pdf"
            d.metadata["source"] = f"data/{path.name}"
            docs.append(d)
    for path in sorted(DATA_DIR.glob("*.md")):
        for d in TextLoader(str(path), encoding="utf-8").load():
            d.metadata["doc_type"] = "markdown"
            d.metadata["source"] = f"data/{path.name}"
            docs.append(d)
    return docs


def split_docs(docs, chunk_size=800, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
    )
    chunks = splitter.split_documents(docs)
    for i, c in enumerate(chunks):
        c.metadata["chunk_id"] = i
    return chunks


def build_index(chunks):
    vs = get_vectorstore()
    ids = [f"{c.metadata['source']}::{c.metadata['chunk_id']}" for c in chunks]
    existing = set(vs.get()["ids"])
    fresh_docs = []
    fresh_ids = []
    for chunk, chunk_id in zip(chunks, ids):
        if chunk_id not in existing:
            fresh_docs.append(chunk)
            fresh_ids.append(chunk_id)
    if fresh_docs:
        vs.add_documents(fresh_docs, ids=fresh_ids)
    return vs


def ensure_index():
    vs = get_vectorstore()
    if vs._collection.count() == 0:
        vs = build_index(split_docs(load_corpus(), 800, 100))
    return vs


TEST_SET = [
    {"question": "How many days of annual leave does a full-time employee receive?", "source": "data/leave-policy.md"},
    {"question": "What is the yearly vacation allowance for a full-time employee?", "source": "data/leave-policy.md"},
    {"question": "What does PTO mean?", "source": "data/leave-policy.md"},
    {"question": "What prefix does every support ticket start with?", "source": "data/handbook.md"},
    {"question": "Who founded Northwind Studio?", "source": "data/handbook.md"},
    {"question": "How much does Lumen Draft cost per seat each month?", "source": "data/handbook.md"},
    {"question": "Which team handles the weekend on-call shift?", "source": "data/handbook.md"},
    {"question": "How long are uploaded documents kept?", "source": "data/handbook.md"},
    {"question": "What is the name of the VPN client?", "source": "data/onboarding.md"},
    {"question": "Within how many hours must a lost badge be reported?", "source": "data/security-policy.pdf"},
]

def evaluate_retriever(retriever, test_set):
    hits, rr, misses = 0, 0.0, []
    for item in test_set:
        docs = retriever.invoke(item["question"])
        sources = [d.metadata.get("source") for d in docs]
        rank = next((i for i, s in enumerate(sources, start=1) if s == item["source"]), None)
        if rank:
            hits += 1
            rr += 1 / rank
        else:
            misses.append(item["question"])
    n = len(test_set)
    return {"hit_rate": hits / n, "mrr": rr / n, "misses": misses}

vs = ensure_index()
print("800/100", evaluate_retriever(vs.as_retriever(search_kwargs={"k": 4}), TEST_SET))

small = split_docs(load_corpus(), 400, 50)
vs_small = Chroma(
    collection_name="corpus_400",
    embedding_function=get_embeddings(),
    persist_directory=PERSIST_DIR,
)
ids = [f"{c.metadata['source']}::{c.metadata['chunk_id']}" for c in small]
existing = set(vs_small.get()["ids"])
fresh_docs = []
fresh_ids = []
for chunk, chunk_id in zip(small, ids):
    if chunk_id not in existing:
        fresh_docs.append(chunk)
        fresh_ids.append(chunk_id)
if fresh_docs:
    vs_small.add_documents(fresh_docs, ids=fresh_ids)

print("400/50", evaluate_retriever(vs_small.as_retriever(search_kwargs={"k": 4}), TEST_SET))
