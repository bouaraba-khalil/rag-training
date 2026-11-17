import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_chroma import Chroma
from langchain_cohere import CohereEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

load_dotenv()

os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")


llm = init_chat_model("cohere:command-a-03-2025", temperature=0)

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



def doc_key(d):
    return str(d.metadata.get("source")) + "::" + str(d.metadata.get("chunk_id"))


questions = [
    "What is the yearly vacation allowance for a full-time employee?",
    "What does the acronym PTO stand for?",
    "Who founded Northwind Studio, and which team covers the weekend on-call shift?",
]

def hybrid_retriever(chunks, vector_retriever, k=4, c=60):
    bm25 = BM25Retriever.from_documents(chunks)
    bm25.k = k * 2

    def run(question):
        scores, by_key = {}, {}
        for results in (vector_retriever.invoke(question), bm25.invoke(question)):
            for rank, d in enumerate(results):
                key = doc_key(d)
                by_key[key] = d
                scores[key] = scores.get(key, 0) + 1 / (c + rank + 1)
        ranked = sorted(scores, key=scores.get, reverse=True)
        return [by_key[key] for key in ranked[:k]]

    return RunnableLambda(run)

def llm_filter(base_retriever, llm):
    judge = ChatPromptTemplate.from_template(
        "Question: {question}\n\n"
        "Passage:\n"
        "{passage}\n\n"
        "Does the passage help answer the question? Reply with yes or no only."
    ) | llm | StrOutputParser()

    def run(question):
        kept = []
        for d in base_retriever.invoke(question):
            verdict = judge.invoke({"question": question, "passage": d.page_content})
            if verdict.strip().lower().startswith("yes"):
                kept.append(d)
        return kept

    return RunnableLambda(run)

chunks = split_docs(load_corpus(), 800, 100)  # same settings as the index, so chunk ids match
vs = ensure_index()
hybrid = hybrid_retriever(chunks, vs.as_retriever(search_kwargs={"k": 8}), k=4)
retrievers = {
    "hybrid": hybrid,
    "hybrid+filter": llm_filter(hybrid, llm),
}

for q in questions:
    print()
    print("Q:", q)
    for name, retriever in retrievers.items():
        ids = [doc_key(d).split("::")[-1] for d in retriever.invoke(q)]
        print(f"  {name:14s}", ids)
