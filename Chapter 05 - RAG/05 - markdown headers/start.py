from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

HANDBOOK = Path(__file__).resolve().parents[1] / "data" / "handbook.md"

text = HANDBOOK.read_text(encoding="utf-8")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
chunks = splitter.split_text(text)

for chunk in chunks[:3]:
    print("---")
    print(chunk[:150])
