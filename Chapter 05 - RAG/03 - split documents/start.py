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
for d in docs:
    print(d.metadata["source"], len(d.page_content), "chars")
