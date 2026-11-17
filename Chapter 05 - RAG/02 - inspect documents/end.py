from collections import Counter
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


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
print(Counter(d.metadata["doc_type"] for d in docs))

seen = set()
for d in docs:
    doc_type = d.metadata["doc_type"]
    if doc_type not in seen:
        seen.add(doc_type)
        print("---", doc_type, d.metadata)
        print(d.page_content[:300])
