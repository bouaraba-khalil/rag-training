import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_chroma import Chroma
from langchain_cohere import CohereEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
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

def multi_query_retriever(base_retriever, llm, n=3, limit=6):
    prompt = ChatPromptTemplate.from_template(
        "Rewrite the question in {n} different ways, using different wording.\n"
        "Return one rewrite per line and nothing else.\n\n"
        "Question: {question}"
    )
    rewriter = prompt | llm | StrOutputParser()

    def run(question):
        lines = rewriter.invoke({"question": question, "n": n}).splitlines()
        queries = [question] + [ln.strip() for ln in lines if ln.strip()]
        seen, merged = set(), []
        for query in queries:
            for d in base_retriever.invoke(query):
                if doc_key(d) not in seen:
                    seen.add(doc_key(d))
                    merged.append(d)
        return merged[:limit]

    return RunnableLambda(run)

vs = ensure_index()
retrievers = {
    "baseline": vs.as_retriever(search_kwargs={"k": 4}),
    "multi-query": multi_query_retriever(vs.as_retriever(search_kwargs={"k": 4}), llm),
}

for q in questions:
    print()
    print("Q:", q)
    for name, retriever in retrievers.items():
        ids = [doc_key(d).split("::")[-1] for d in retriever.invoke(q)]
        print(f"  {name:14s}", ids)
