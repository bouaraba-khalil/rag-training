import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_chroma import Chroma
from langchain_cohere import CohereEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough, RunnableWithMessageHistory
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



rewrite_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Rewrite the latest user question so it can be understood without the conversation. "
        "Resolve words like 'it' and 'the second one' using the conversation. "
        "Return one question on a single line. Do not answer it. "
        "If it is already standalone, return it unchanged.",
    ),
    MessagesPlaceholder("chat_history"),
    ("human", "{question}"),
])

answer_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),
    MessagesPlaceholder("chat_history"),
    ("human", "{question}"),
])


def build_conversational_chain(retriever, llm):
    rewriter = rewrite_prompt | llm | StrOutputParser()

    def standalone(x):
        if not x["chat_history"]:
            return x["question"]
        return rewriter.invoke(x)

    def retrieve(x):
        return retriever.invoke(x["standalone"])

    answer_chain = (
        RunnableLambda(lambda x: {**x, "context": format_docs(x["docs"])})
        | answer_prompt
        | llm
        | StrOutputParser()
    )

    return (
        RunnablePassthrough.assign(chat_history=lambda x: x["chat_history"][-6:])
        | RunnablePassthrough.assign(standalone=RunnableLambda(standalone))
        | RunnablePassthrough.assign(docs=RunnableLambda(retrieve))
        | RunnablePassthrough.assign(answer=answer_chain)
    )


_store = {}


def get_history(session_id):
    if session_id not in _store:
        _store[session_id] = InMemoryChatMessageHistory()
    return _store[session_id]


def with_memory(chain):
    return RunnableWithMessageHistory(
        chain,
        get_history,
        input_messages_key="question",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )


retriever = ensure_index().as_retriever(search_kwargs={"k": 4})
bot = with_memory(build_conversational_chain(retriever, llm))
demo = {"configurable": {"session_id": "demo"}}
other = {"configurable": {"session_id": "other"}}

turns = [
    "What are the two Lumen products?",
    "And what about the second one?",
    "Can you give more details on it?",
]
for question in turns:
    out = bot.invoke({"question": question}, config=demo)
    print()
    print("USER      :", question)
    print("STANDALONE:", out["standalone"])
    print("ANSWER    :", out["answer"])

print()
print("demo messages:", len(get_history("demo").messages))

out = bot.invoke({"question": "What is the name of the VPN client?"}, config=other)
print("OTHER STANDALONE:", out["standalone"])
print("other messages:", len(get_history("other").messages))
print("demo messages:", len(get_history("demo").messages))
