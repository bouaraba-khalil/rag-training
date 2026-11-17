from pathlib import Path
from statistics import mean

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

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


docs = load_corpus()

for size, overlap in [(200, 0), (800, 100), (1500, 200)]:
    chunks = split_docs(docs, size, overlap)
    lengths = [len(c.page_content) for c in chunks]
    print(f"size={size} overlap={overlap}: {len(chunks)} chunks, mean={mean(lengths):.0f}, max={max(lengths)}")

small = split_docs(docs, 200, 0)
large = split_docs(docs, 1500, 200)

print()
print("smallest setting:")
for c in small[:3]:
    print("-", c.page_content[:120].replace("\n", " "))

print()
print("largest setting:")
for c in large[:3]:
    print("-", c.page_content[:120].replace("\n", " "))
