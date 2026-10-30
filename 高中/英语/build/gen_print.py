# -*- coding: utf-8 -*-
"""生成打印版 HTML（封面 + 目录 + 全部单元卡片），供 Chrome 打印成 PDF。"""
import json
import pathlib
import re
import sys

import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
CARDS = ROOT / "data" / "考点库.json"
OUT = ROOT / "输出" / "_print_cards.html"


def main():
    d = json.loads(CARDS.read_text(encoding="utf-8"))
    cards, toc, last = [], [], ""
    for b in d["books"]:
        toc.append(f'<div class="toc-book">{b["title"]}</div>')
        for c in b["cards"]:
            body = "\n".join(ln for ln in c["body"].splitlines()
                             if not (ln.strip().startswith("*") and ln.strip().endswith("*") and len(ln.strip()) > 2))
            html = markdown.markdown(body, extensions=["tables", "sane_lists"])
            cards.append(f'<article class="pcard"><h2>{c["id"]}　{c["name"]}</h2>{html}</article>')
            toc.append(f'<div class="toc-line"><span>{c["id"]}</span><span>{c["name"]}</span></div>')

    doc = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<title>上海高中英语知识图谱手册</title><style>
@page {{ size:A4; margin:12mm 12mm 14mm; }}
body {{ margin:0; color:#111; font:9.2pt/1.6 "Songti SC",SimSun,-apple-system,sans-serif; }}
.cover {{ height:250mm; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; page-break-after:always; }}
.cover h1 {{ font-size:27pt; color:#0b6b5b; letter-spacing:3mm; margin:3mm; }}
.cover .sub {{ font-size:11pt; color:#444; }}
.cover .meta {{ font-size:9pt; color:#777; margin-top:8mm; }}
.toc {{ page-break-after:always; column-count:2; column-gap:8mm; }}
.toc h2 {{ column-span:all; color:#0b6b5b; font-size:15pt; margin:0 0 4mm; }}
.toc-book {{ color:#0b6b5b; font-weight:700; margin-top:2.5mm; break-after:avoid; }}
.toc-line {{ display:flex; gap:4mm; font-size:8.6pt; line-height:1.5; padding-left:3mm; }}
.toc-line span:first-child {{ width:13mm; color:#666; }}
.pcard {{ page-break-before:always; }}
.pcard h2 {{ font-size:14pt; color:#0b6b5b; border-bottom:1px solid #0b6b5b; padding-bottom:1mm; margin:0 0 2mm; }}
.pcard h3 {{ font-size:10.5pt; color:#14532d; margin:4mm 0 1.2mm; padding-left:6px; border-left:3px solid #0b6b5b; }}
.pcard p {{ margin:1.2mm 0; text-align:justify; }}
.pcard ul, .pcard ol {{ margin:1mm 0 1mm 5mm; padding:0; }}
.pcard li {{ margin:0.6mm 0; }}
.pcard table {{ border-collapse:collapse; width:100%; font-size:8.4pt; margin:2mm 0; }}
.pcard th, .pcard td {{ border:1px solid #d9d9d9; padding:1.2mm 1.6mm; vertical-align:top; }}
.pcard th {{ background:#eef4f1; }}
.pcard blockquote {{ margin:2mm 0; background:#f4f7f5; border-left:3px solid #0b6b5b; padding:1.2mm 3mm; }}
.pcard strong {{ color:#0f3d33; }}
</style></head><body>
<section class="cover"><h1>上海高中英语</h1><h1>知 识 图 谱</h1>
<div class="sub">沪教版 2022 · 必修 1–3 ｜ 选择性必修 1–4</div>
<div class="meta">{d['stats']['cards']} 个单元 ｜ 1560 词条 ｜ 7 篇故事（见词汇默写本）</div></section>
<section class="toc"><h2>目　录</h2>{''.join(toc)}</section>
{''.join(cards)}
</body></html>"""
    OUT.write_text(doc, encoding="utf-8")
    print("saved", OUT, len(doc) // 1024, "KB")


if __name__ == "__main__":
    main()
