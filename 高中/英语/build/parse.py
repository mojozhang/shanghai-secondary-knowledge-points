# -*- coding: utf-8 -*-
"""解析英语单元卡片 Markdown → data/考点库.json"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "考点库.json"
sys.path.insert(0, str(ROOT / "build"))
import units_meta  # noqa: E402

CARD_RE = re.compile(r"^## (E-\d+\.\d+)\s+(.+?)\s*$", re.M)
SEC_RE = re.compile(r"^### (.+?)\s*$", re.M)
UNIT_RE = re.compile(r"^# (.+?)\s*$", re.M)


def sections(block):
    parts = SEC_RE.split(block)
    out = []
    for i in range(1, len(parts), 2):
        out.append({"title": parts[i].strip(), "body": parts[i + 1].strip()})
    return out


def parse_book(path):
    text = path.read_text(encoding="utf-8")
    m = UNIT_RE.search(text)
    book_title = m.group(1).strip() if m else path.stem
    heads = list(CARD_RE.finditer(text))
    cards = []
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        block = text[h.end():end]
        cid, name = h.group(1), h.group(2).strip()
        meta = ""
        for ln in block.splitlines():
            s = ln.strip()
            if s.startswith("*") and s.endswith("*") and len(s) > 2:
                meta = s.strip("*")
                break
        guess = ""
        g = re.search(r"\*\*⚡ 先猜\*\*[：:]\s*(.+)", block)
        if g:
            guess = g.group(1).strip()
        cards.append({
            "id": cid, "name": name, "book_title": book_title,
            "meta": meta, "guess": guess,
            "sections": sections(block), "body": block.strip(), "file": path.name,
        })
    return {"title": book_title, "file": path.name, "cards": cards}


def main():
    files = sorted(p for p in ROOT.glob("0[1-7]-*.md"))
    books = [parse_book(p) for p in files if CARD_RE.search(p.read_text(encoding="utf-8"))]
    data = {
        "books": books,
        "stats": {
            "books": len(books),
            "cards": sum(len(b["cards"]) for b in books),
            "sections": sum(len(c["sections"]) for b in books for c in b["cards"]),
        },
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    s = data["stats"]
    print(f"books={s['books']} cards={s['cards']} sections={s['sections']}")
    for b in books:
        print(" -", b["file"], len(b["cards"]), "cards")


if __name__ == "__main__":
    main()
