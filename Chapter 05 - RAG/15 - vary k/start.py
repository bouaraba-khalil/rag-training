import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_chroma import Chroma
from langchain_cohere import CohereEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")


llm = init_chat_model("cohere:command-a-03-2025", temperature=0)

CHAPTER_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = CHAPTER_DIR / "data"
PERSIST_DIR = str(CHAPTER_DIR / "chroma_db")

REFUSAL = "I do not know based on the provided documents."

SYSTEM = """You are a careful assistant. Answer the question using ONLY the context below.
Cite the passages you used as [1], [2], and so on.
If the context does not contain the answer, reply exactly: """ + REFUSAL + """

Context:
{context}"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),
    ("human", "{question}"),
])


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


def format_docs(docs):
    parts = []
    for i, d in enumerate(docs, start=1):
        src = d.metadata.get("source")
        page = d.metadata.get("page", "n/a")
        parts.append(f"[{i}] (source: {src}, page: {page})\n{d.page_content}")
    return "\n\n".join(parts)


def build_rag_chain(retriever, llm):
    answer_chain = (
        RunnableLambda(lambda x: {"context": format_docs(x["docs"]), "question": x["question"]})
        | prompt
        | llm
        | StrOutputParser()
    )
    return (
        RunnableParallel(docs=retriever, question=RunnablePassthrough())
        | RunnablePassthrough.assign(answer=answer_chain)
    )


def show(result):
    print(result["answer"])
    print("Sources:")
    for d in result["docs"]:
        print(" -", d.metadata.get("source"), d.metadata.get("page", ""))


def make_chain(k):
    retriever = ensure_index().as_retriever(search_kwargs={"k": k})
    return build_rag_chain(retriever, llm)


question = "Who founded Northwind Studio, and which team covers the weekend on-call shift?"
print("k = 4")
show(make_chain(4).invoke(question))
