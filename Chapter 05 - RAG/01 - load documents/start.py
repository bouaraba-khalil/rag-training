from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

for path in sorted(DATA_DIR.iterdir()):
    print(path.name, path.stat().st_size, "bytes")

text = (DATA_DIR / "handbook.md").read_text(encoding="utf-8")
print(text[:300])
