# -*- coding: utf-8 -*-
"""生成 Word 手册：封面 → 目录 → 单元卡片。"""
import json
import pathlib
import re

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = pathlib.Path(__file__).resolve().parent.parent
CARDS = json.loads((ROOT / "data" / "考点库.json").read_text(encoding="utf-8"))
OUT = ROOT / "输出" / "上海高中英语知识图谱手册.docx"
GREEN = RGBColor(0x0B, 0x6B, 0x5B)
DARK = RGBColor(0x14, 0x53, 0x2D)


def font(run, size=9.5, bold=False, color=None, ea="宋体", ascii_="Calibri"):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = ascii_
    run._element.rPr.rFonts.set(qn("w:eastAsia"), ea)
    if color is not None:
        run.font.color.rgb = color


def rich(p, text, size=9.2, bold=False, color=None):
    for seg in re.split(r"(\*\*[^*]+\*\*)", text):
        if not seg:
            continue
        if seg.startswith("**") and seg.endswith("**"):
            r = p.add_run(seg[2:-2]); font(r, size, True, color)
        else:
            r = p.add_run(seg); font(r, size, bold, color)


def para(doc, text="", size=9.2, bold=False, color=None, indent=0, before=0.5, after=0.5):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.15
    if indent:
        p.paragraph_format.left_indent = Cm(indent)
    rich(p, text, size, bold, color)
    return p


def add_table(doc, rows):
    n = max(len(r) for r in rows)
    t = doc.add_table(rows=0, cols=n)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(rows):
        cells = t.add_row().cells
        for j in range(n):
            txt = row[j] if j < len(row) else ""
            p = cells[j].paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            rich(p, txt.replace("**", ""), 8.2, i == 0)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def render(doc, md):
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1; continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                s = lines[i].strip().strip("|")
                cells = [c.strip() for c in s.split("|")]
                if not all(set(c) <= set("-: ") and c for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                add_table(doc, rows)
            continue
        if ln.startswith("### "):
            para(doc, ln[4:], 10.5, True, DARK, before=6, after=2)
        elif ln.startswith("- "):
            para(doc, "• " + ln[2:], 9.2, indent=0.35, before=0, after=0)
        elif ln.startswith("> "):
            para(doc, ln[2:], 9.2, False, RGBColor(0x33, 0x33, 0x33), indent=0.35)
        elif re.match(r"^\d+\.\s", ln):
            para(doc, ln, 9.2, indent=0.35, before=0, after=0)
        else:
            para(doc, ln, 9.2)
        i += 1


def main():
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Cm(1.8); sec.bottom_margin = Cm(1.6)
    sec.left_margin = Cm(2.0); sec.right_margin = Cm(2.0)

    for _ in range(3):
        doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("上海高中英语"); font(r, 26, True, GREEN, ea="黑体")
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("知 识 图 谱"); font(r, 26, True, GREEN, ea="黑体")
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("沪教版 2022 · 必修 1–3 ｜ 选择性必修 1–4"); font(r, 10.5, False, RGBColor(0x44, 0x44, 0x44))
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f"{CARDS['stats']['cards']} 个单元 · 1560 词条 · 5 勾间隔复习"); font(r, 9, False, RGBColor(0x77, 0x77, 0x77))
    doc.add_page_break()

    for b in CARDS["books"]:
        doc.add_heading(b["title"], level=1)
        for c in b["cards"]:
            doc.add_heading(f"{c['id']}　{c['name']}", level=2)
            body = "\n".join(ln for ln in c["body"].splitlines()
                             if not (ln.strip().startswith("*") and ln.strip().endswith("*") and len(ln.strip()) > 2))
            render(doc, body)
    OUT.parent.mkdir(exist_ok=True)
    doc.save(OUT)
    print("saved", OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
