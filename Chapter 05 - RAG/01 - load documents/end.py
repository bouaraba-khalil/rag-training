import os
from pathlib import Path

os.environ["USER_AGENT"] = "rag-training"

from langchain_community.document_loaders import PyPDFLoader, TextLoader, WebBaseLoader

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
WEB_URLS = ["https://lilianweng.github.io/posts/2023-06-23-agent/"]


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


docs = load_corpus()
print("local documents:", len(docs))
for d in docs:
    print(d.metadata["doc_type"], d.metadata["source"], "chars", len(d.page_content))

try:
    web_docs = WebBaseLoader(WEB_URLS).load()
except Exception as exc:
    web_docs = []
    print("web load skipped:", exc)

for d in web_docs:
    d.metadata["doc_type"] = "web"
    print("web", d.metadata.get("source"), "chars", len(d.page_content))
