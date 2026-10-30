# -*- coding: utf-8 -*-
"""检查每篇故事对本册词表的覆盖情况。"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
import vocab  # noqa: E402

STORY = ROOT / "data" / "故事.json"


def forms(word):
    w = re.escape(word)
    if " " in word:
        return [re.compile(re.escape(word), re.I)]
    pats = [re.compile(r"\b" + w + r"(s|es|ed|d|ing|ly|er|est|ies|ied)?\b", re.I)]
    if len(word) > 2 and word[-1].isalpha():
        pats.append(re.compile(r"\b" + re.escape(word[:-1]) + re.escape(word[-1]) + re.escape(word[-1])
                               + r"(ed|ing|er|est)\b", re.I))
    return pats


def main():
    stories = json.loads(STORY.read_text(encoding="utf-8"))
    bu = vocab.by_unit()
    total_missing = 0
    for book_no, st in sorted(stories.items(), key=lambda x: int(x[0])):
        text = " ".join(c["text"] for c in st["chapters"]).replace("**", "")
        words = []
        for u in range(1, 5):
            words += [r["word"] for r in bu.get(f"E-{book_no}.{u}", [])]
        words = list(dict.fromkeys(words))
        miss = [w for w in words
                if not any(p.search(text) for p in forms(w))]
        total_missing += len(miss)
        print(f"book {book_no}: {len(words)-len(miss)}/{len(words)} covered, "
              f"{len(text.split())} words, missing: {', '.join(miss) if miss else '—'}")
    print("total missing:", total_missing)


if __name__ == "__main__":
    main()
