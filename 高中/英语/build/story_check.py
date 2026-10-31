# -*- coding: utf-8 -*-
"""检查每篇故事对本册词表的覆盖情况，并生成 data/故事覆盖报告.md。

两个口径：

- 词形覆盖（默认）：原形，或常见屈折/派生形（-s/-es/-ed/-ing/-ly/-er/-est/
  -ies/-ied/-ion/-ment/-ness）出现即算覆盖。
- 原形覆盖（--strict）：必须出现原形本身，仅屈折形算未覆盖。

退出码：默认有任何缺失即 1；--strict 下"仅屈折"也算失败。
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
import vocab  # noqa: E402

STORY = ROOT / "data" / "故事.json"
REPORT = ROOT / "data" / "故事覆盖报告.md"
BOOK_NAMES = {
    1: "必修一", 2: "必修二", 3: "必修三", 4: "选必一",
    5: "选必二", 6: "选必三", 7: "选必四",
}


def forms(word):
    """原形 + 屈折/派生形的匹配式。"""
    w = re.escape(word)
    if " " in word:
        return [re.compile(re.escape(word), re.I)]
    pats = [re.compile(r"\b" + w + r"(s|es|ed|d|ing|ly|er|ers|est|ies|ied|ion|ions|ment|ments|ness)?\b", re.I)]
    if len(word) > 2 and word[-1].isalpha():
        pats.append(re.compile(r"\b" + re.escape(word[:-1]) + re.escape(word[-1]) + re.escape(word[-1])
                               + r"(ed|ing|er|est)\b", re.I))
    return pats


def base_form(word):
    """只匹配原形（整词边界，大小写不敏感）。"""
    return re.compile(r"(?<![A-Za-z])" + re.escape(word) + r"(?![A-Za-z])", re.I)


def check_book(book_no, story, unit_words):
    text = " ".join(c["text"] for c in story["chapters"]).replace("**", "")
    base, only_derived, missing = [], [], []
    for word in unit_words:
        if base_form(word).search(text):
            base.append(word)
        elif any(p.search(text) for p in forms(word)):
            only_derived.append(word)
        else:
            missing.append(word)
    return {
        "book_no": book_no,
        "title": story.get("title", ""),
        "words": len(unit_words),
        "base": base,
        "only_derived": only_derived,
        "missing": missing,
        "text_words": len(text.split()),
    }


def main():
    strict = "--strict" in sys.argv[1:]
    stories = json.loads(STORY.read_text(encoding="utf-8"))
    bu = vocab.by_unit()

    rows = []
    for book_no, story in sorted(stories.items(), key=lambda x: int(x[0])):
        words = []
        for u in range(1, 5):
            words += [r["word"] for r in bu.get(f"E-{book_no}.{u}", [])]
        words = list(dict.fromkeys(words))
        rows.append(check_book(book_no, story, words))

    total = sum(r["words"] for r in rows)
    total_base = sum(len(r["base"]) for r in rows)
    total_derived = sum(len(r["only_derived"]) for r in rows)
    total_missing = sum(len(r["missing"]) for r in rows)

    for r in rows:
        print(f"book {r['book_no']} ({BOOK_NAMES.get(int(r['book_no']), '')}): "
              f"原形 {len(r['base'])}/{r['words']} ｜ 仅屈折 {len(r['only_derived'])} ｜ "
              f"缺失 {len(r['missing'])} ｜ 正文 {r['text_words']} 词")
        if r["missing"]:
            print(f"    missing: {', '.join(r['missing'])}")
    print(f"合计: 原形 {total_base}/{total} ｜ 仅屈折 {total_derived} ｜ 缺失 {total_missing}")

    REPORT.write_text(render_report(rows, total, total_base, total_derived), encoding="utf-8")
    print(f"报告已写入 {REPORT.relative_to(ROOT)}")

    failed = total_missing > 0 or (strict and total_derived > 0)
    if strict and total_derived:
        print(f"[strict] {total_derived} 个词没有以原形出现")
    sys.exit(1 if failed else 0)


def render_report(rows, total, total_base, total_derived):
    lines = [
        "# 故事覆盖报告（自动生成，勿手改）",
        "",
        "> 生成命令：`python3 build/story_check.py`；严格口径：`--strict`。",
        "> 判定口径：**词形覆盖** = 原形或常见屈折/派生形出现即算；**原形覆盖** = 必须出现原形本身。",
        "",
        "## 总览",
        "",
        "| 册 | 故事 | 词条 | 原形出现 | 仅屈折 | 词形覆盖 | 缺失 | 正文词数 |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        covered = len(r["base"]) + len(r["only_derived"])
        lines.append(
            f"| {BOOK_NAMES.get(int(r['book_no']), r['book_no'])} | {r['title']} | {r['words']} | "
            f"{len(r['base'])} | {len(r['only_derived'])} | {covered}/{r['words']} | "
            f"{len(r['missing'])} | {r['text_words']} |"
        )
    lines += [
        f"| **合计** | — | **{total}** | **{total_base}** | **{total_derived}** | "
        f"**{total - sum(len(r['missing']) for r in rows)}/{total}** | "
        f"**{sum(len(r['missing']) for r in rows)}** | "
        f"**{sum(r['text_words'] for r in rows)}** |",
        "",
        "## 仅以屈折/派生形出现的词",
        "",
        "这些词在故事里只出现了屈折或派生形式（如 `**kidnap**ped`），原形未单独出现；",
        "阅读时词根已加粗，认词不受影响，但按 `--strict` 口径不计覆盖。",
        "",
    ]
    for r in rows:
        name = BOOK_NAMES.get(int(r["book_no"]), r["book_no"])
        if r["only_derived"]:
            lines += [f"### {name} · {r['title']}（{len(r['only_derived'])} 个）", "",
                      "、".join(f"`{w}`" for w in r["only_derived"]), ""]
        else:
            lines += [f"### {name} · {r['title']}", "", "无。", ""]
    if any(r["missing"] for r in rows):
        lines += ["## 缺失", ""]
        for r in rows:
            if r["missing"]:
                lines.append(f"- {BOOK_NAMES.get(int(r['book_no']), r['book_no'])}："
                             + "、".join(f"`{w}`" for w in r["missing"]))
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
