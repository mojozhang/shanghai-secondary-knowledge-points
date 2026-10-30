# -*- coding: utf-8 -*-
"""生成《上海高中英语 · 词汇默写本》HTML（再由 Chrome 打印成 PDF）。"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
import units_meta  # noqa: E402
import vocab  # noqa: E402

OUT = ROOT / "输出" / "_vocab_book.html"
STORIES = ROOT / "data" / "故事.json"


def esc(s):
    return html.escape(s, quote=False)


def bold(s):
    """转义后把 **词** 变成加粗。"""
    out = []
    pos = 0
    for m in re.finditer(r"\*\*(.+?)\*\*", s):
        out.append(esc(s[pos:m.start()]))
        out.append("<b>" + esc(m.group(1)) + "</b>")
        pos = m.end()
    out.append(esc(s[pos:]))
    return "".join(out)


def boxes():
    return '<span class="bxs">' + "".join('<span class="bx"></span>' for _ in range(5)) + "</span>"


def row(r, idx, show_tag=False):
    tag = ""
    if show_tag:
        if "unit" in r:
            code = f'{r["book_no"]}.{r["unit"]}'
        else:
            code = r["units"][0].replace("E-", "")
        tag = f'<span class="tag">{code}</span>'
    return (f'<tr><td class="no">{idx}</td>'
            f'<td class="en"><b>{esc(r["word"])}</b> <span class="pos">{esc(r["pos_all"])}</span>{tag}</td>'
            f'<td class="bx-cell">{boxes()}</td>'
            f'<td class="cn">{esc(r["cn"])} <span class="pos">{esc(r["pos_all"])}</span></td></tr>')


def unit_table(rows):
    head = ('<table class="vw"><colgroup><col style="width:5%"><col style="width:31%">'
            '<col style="width:23%"><col style="width:41%"></colgroup>'
            '<thead><tr><th>#</th><th>英文（词性）</th>'
            '<th class="th-b">D0&nbsp; D+1&nbsp; D+3&nbsp; D+7&nbsp; D+15</th>'
            '<th>中文（词性）</th></tr></thead><tbody>')
    return head + "".join(row(r, i + 1) for i, r in enumerate(rows)) + "</tbody></table>"


def master_table(rows):
    out, cur = [], ""
    head = ('<colgroup><col style="width:5%"><col style="width:31%">'
            '<col style="width:23%"><col style="width:41%"></colgroup>'
            '<thead><tr><th>#</th><th>英文（词性）</th>'
            '<th class="th-b">D0&nbsp; D+1&nbsp; D+3&nbsp; D+7&nbsp; D+15</th>'
            '<th>中文（词性）</th></tr></thead><tbody>')
    for i, r in enumerate(rows, 1):
        letter = r["word"][0].upper()
        if letter != cur:
            if cur:
                out.append("</tbody></table>")
            cur = letter
            out.append(f'<h3 class="letter">{cur}</h3><table class="vw">{head}')
        out.append(row(r, i, show_tag=True))
    if cur:
        out.append("</tbody></table>")
    return "".join(out)


def story_block(book, story):
    if not story:
        return ""
    parts = []
    for ch in story.get("chapters", []):
        paras = "".join(f"<p>{bold(p)}</p>" for p in ch["text"].strip().split("\n\n"))
        parts.append(f'<h3 class="ch-title">{esc(ch["title"])}</h3><div class="story-text">{paras}</div>')
    return f'''<section class="story">
  <div class="story-kicker">{esc(book['short'])} · 边读边背</div>
  <h2>{esc(story['title'])}</h2>
  <p class="cn-brief">{esc(story.get('cn',''))}</p>
  {''.join(parts)}
  <p class="story-note">加粗词为本册词表目标词；先读故事猜词义，再翻到后面的词表逐词核对与默写。</p>
</section>'''


def build():
    by_unit = vocab.by_unit()
    master = vocab.master()
    stories = json.loads(STORIES.read_text(encoding="utf-8")) if STORIES.exists() else {}
    stats = vocab.stats()

    toc = []
    for b in units_meta.BOOKS:
        for u in b["units"]:
            uid = f"E-{b['no']}.{u['unit']}"
            toc.append(f'<div class="toc-line"><span>{b["short"]} Unit {u["unit"]}</span>'
                       f'<span class="tl-t">{esc(u["title"])}</span>'
                       f'<span class="tl-n">{len(by_unit.get(uid, []))} 词</span></div>')

    body = []
    for b in units_meta.BOOKS:
        story = stories.get(str(b["no"]))
        if story:
            body.append(story_block(b, story))
        for u in b["units"]:
            uid = f"E-{b['no']}.{u['unit']}"
            rows = by_unit.get(uid, [])
            body.append(f'<section class="unit"><h2>{esc(b["short"])} Unit {u["unit"]} '
                        f'<span class="ut">{esc(u["title"])}</span>'
                        f'<span class="uc">{len(rows)} 词</span></h2>'
                        f'<p class="unit-meta">{esc(u["reading"])} ｜ {esc(u["grammar"])}</p>'
                        + unit_table(rows) + '</section>')

    html_doc = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>上海高中英语 · 词汇默写本</title>
<style>
@page {{ size:A4; margin:9mm 8mm 10mm; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; color:#111; font:8.5pt/1.45 "Songti SC","STSong","SimSun",-apple-system,sans-serif; }}
section {{ padding:0; }}
.cover {{ height:250mm; display:flex; flex-direction:column; justify-content:center; align-items:center; page-break-after:always; text-align:center; }}
.cover h1 {{ font-size:26pt; color:#0b6b5b; margin:3mm 0; letter-spacing:2mm; }}
.cover .sub {{ font-size:11pt; color:#444; margin:2mm; }}
.cover .meta {{ font-size:9pt; color:#777; margin-top:8mm; }}
.intro {{ page-break-after:always; }}
.intro h2 {{ font-size:14pt; color:#0b6b5b; border-left:4px solid #0b6b5b; padding-left:6px; margin:4mm 0 3mm; }}
.intro h3 {{ font-size:10.5pt; margin:4mm 0 1.5mm; }}
.intro p, .intro li {{ font-size:9pt; line-height:1.6; }}
.intro table {{ border-collapse:collapse; width:100%; font-size:8.5pt; margin:2mm 0; }}
.intro th,.intro td {{ border:1px solid #d8d8d8; padding:1.2mm 2mm; vertical-align:top; }}
.intro th {{ background:#f1f6f4; }}
.toc {{ page-break-after:always; }}
.toc h2 {{ font-size:13pt; color:#0b6b5b; margin:0 0 3mm; }}
.toc-line {{ display:flex; font-size:8.6pt; line-height:1.5; border-bottom:1px dotted #e2e2e2; padding:0.6mm 0; }}
.toc-line span:first-child {{ width:34mm; color:#0b6b5b; }}
.tl-t {{ flex:1; }}
.tl-n {{ width:16mm; text-align:right; color:#666; }}
.story {{ page-break-before:always; page-break-after:always; }}
.story-kicker {{ font-size:8.5pt; color:#0b6b5b; letter-spacing:1mm; margin-bottom:2mm; }}
.ch-title {{ font-size:11pt; color:#14532d; margin:4mm 0 1.5mm; }}
.story h2 {{ font-size:16pt; margin:0 0 2mm; color:#14532d; }}
.cn-brief {{ font-size:9pt; color:#555; background:#f6f7f4; padding:2mm 3mm; border-left:3px solid #0b6b5b; }}
.story-text p {{ font-size:10.2pt; line-height:1.75; text-align:justify; margin:0 0 2.4mm; font-family:"Georgia","Times New Roman",serif; }}
.story-text b {{ color:#0b6b5b; }}
.story-note {{ font-size:8pt; color:#777; margin-top:4mm; }}
.unit {{ margin-top:6mm; }}
.unit h2 {{ break-after:avoid; font-size:12pt; color:#0b6b5b; border-left:4px solid #0b6b5b; padding-left:6px; margin:0 0 1mm; }}
.ut {{ color:#111; font-weight:400; margin-left:3mm; }}
.uc {{ float:right; font-size:8.5pt; color:#666; font-weight:400; }}
.unit-meta {{ font-size:7.8pt; color:#777; margin:0 0 2mm 10px; }}
table.vw {{ width:100%; border-collapse:collapse; table-layout:fixed; font-size:8.2pt; }}
table.vw thead {{ display:table-header-group; }}
table.vw th {{ background:#eef4f1; border-bottom:1px solid #b9c9c2; padding:1mm 1.4mm; text-align:left; font-weight:600; font-size:7.8pt; }}
table.vw td {{ border-bottom:0.5px dotted #c9c9c9; padding:1.15mm 1.4mm; vertical-align:middle; }}
table.vw tr {{ page-break-inside:avoid; }}
.no {{ color:#999; font-size:7.4pt; text-align:right; padding-right:1mm !important; }}
.en b {{ font-family:"Georgia","Times New Roman",serif; font-size:9pt; font-weight:600; }}
.pos {{ color:#777; font-size:7.4pt; }}
.tag {{ color:#b45309; font-size:6.8pt; margin-left:1.5mm; }}
.cn {{ line-height:1.35; }}
.bx-cell {{ white-space:nowrap; }}
.bxs {{ display:inline-block; }}
.bx {{ display:inline-block; width:3.3mm; height:3.3mm; border:0.6px solid #999; margin-right:1.15mm; vertical-align:-0.4mm; }}
.th-b {{ font-weight:500; color:#3b5b50; letter-spacing:0.1mm; }}
.letter {{ font-size:13pt; color:#0b6b5b; margin:5mm 0 1mm; border-bottom:1.5px solid #0b6b5b; }}
.master {{ page-break-before:always; }}
.wrong {{ page-break-before:always; }}
.wrong h2 {{ font-size:13pt; color:#0b6b5b; }}
.wtable {{ border-collapse:collapse; width:100%; font-size:8pt; }}
.wtable th,.wtable td {{ border:0.6px solid #bbb; height:8mm; }}
.wtable th {{ background:#f1f6f4; }}
.strips {{ page-break-before:always; }}
.strip {{ height:30mm; border:1px dashed #999; margin:0 0 5mm; display:flex; align-items:center; justify-content:center; color:#666; font-size:9pt; }}
</style></head><body>

<section class="cover">
  <h1>词汇默写本</h1>
  <div class="sub">上海高中英语 · 沪教版 2022</div>
  <div class="sub">必修 1–3 ｜ 选择性必修 1–4</div>
  <div class="meta">{stats['entries']} 个词条 ｜ {stats['unique']} 个不重复单词 ｜ 28 个单元 ｜ 7 篇故事</div>
  <div class="meta">5 个勾 = 5 次间隔复习：D0 · D+1 · D+3 · D+7 · D+15</div>
</section>

<section class="intro">
  <h2>怎么用这本默写本</h2>
  <h3>1. 一行一个词，中间 5 个方框</h3>
  <p>左边是<b>英文 + 词性</b>，最右边是<b>中文 + 词性</b>，中间 5 个方框。<b>盖住右边</b>做英译中，<b>盖住左边</b>做中译英；两个方向都默对，才在当天的格子里打勾。</p>
  <h3>2. 5 个勾不是"打 5 次"，而是 5 个复习节点</h3>
  <p>页眉的 <b>D0 · D+1 · D+3 · D+7 · D+15</b> 就是五个节点：学完当天、次日、第 3 天、第 7 天、第 15 天。哪一次没过，这个词回到 D0 重来。5 个勾全部打满，才算"完全背出"。</p>
  <h3>3. 先读故事，再默词表</h3>
  <p>每册词表前面有一篇英文故事，把本册约 200 个目标词串成一个完整故事，目标词加粗。先读故事猜词义，再翻到后面的词表逐词核对，比直接背词表轻松。</p>
  <h3>4. 遮挡条</h3>
  <p>最后一页有两条可剪下来的遮挡条：一条盖住中文，一条盖住英文；也可以直接用一张卡片横着挡。</p>
  <table><tr><th>符号</th><th>含义</th></tr>
  <tr><td>D0–D+15</td><td>五个复习节点，每格打勾代表该次双向默写通过</td></tr>
  <tr><td>词性</td><td>n. 名词 / v. 动词 / adj. 形容词 / adv. 副词 / prep. 介词 / conj. 连词 / num. 数词 / phr. 短语</td></tr>
  <tr><td>斜体小字（如 3.1）</td><td>该词首次出现的册.单元，如 3.1 = 必修三 Unit 1</td></tr>
  </table>
</section>

<section class="toc">
  <h2>目录</h2>
  {''.join(toc)}
</section>

{''.join(body)}

<section class="master">
  <h2 style="font-size:14pt;color:#0b6b5b;border-left:4px solid #0b6b5b;padding-left:6px;margin:0 0 3mm">总词表（A–Z，{len(master)} 词）</h2>
  <p style="font-size:8.5pt;color:#666;margin:0 0 2mm">同一单词只在首次出现处列一条，释义已合并；单词后的斜体小字（如 3.1）表示首次出现的册.单元。</p>
  {master_table(master)}
</section>

<section class="wrong">
  <h2>错词登记表</h2>
  <p style="font-size:8.5pt;color:#666">默错的词抄在这里，标上日期和错因（拼写 / 词义 / 词性 / 搭配），D+1 和 D+3 各回炉一次。</p>
  <table class="wtable">
    <tr><th style="width:8%">日期</th><th style="width:18%">单词</th><th style="width:30%">正确词义</th><th style="width:14%">错因</th><th style="width:14%">D+1</th><th style="width:14%">D+3</th></tr>
    {''.join('<tr><td></td><td></td><td></td><td></td><td></td><td></td></tr>' for _ in range(22))}
  </table>
</section>

<section class="strips">
  <h2 style="font-size:13pt;color:#0b6b5b">遮挡条（沿虚线剪下）</h2>
  <div class="strip">盖住右侧中文 → 英译中</div>
  <div class="strip">盖住左侧英文 → 中译英</div>
</section>

</body></html>'''
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html_doc, encoding="utf-8")
    print("saved", OUT, len(html_doc) // 1024, "KB")
    return OUT


if __name__ == "__main__":
    build()
