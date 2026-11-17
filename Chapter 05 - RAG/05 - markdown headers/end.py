from pathlib import Path

from langchain_text_splitters import MarkdownHeaderTextSplitter

HANDBOOK = Path(__file__).resolve().parents[1] / "data" / "handbook.md"

text = HANDBOOK.read_text(encoding="utf-8")
splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")]
)

for chunk in splitter.split_text(text)[:3]:
    print(chunk.metadata)
    print(chunk.page_content[:100])
    print()
