# -*- coding: utf-8 -*-
"""生成单文件《上海高中英语知识图谱》HTML：卡片 + 交互词汇表 + 打印版。"""
import html
import json
import pathlib
import sys

import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
import units_meta  # noqa: E402

CARDS = ROOT / "data" / "考点库.json"
VOCAB = ROOT / "data" / "词汇库.json"
OUT = ROOT / "输出" / "上海高中英语知识图谱.html"


def md(text):
    return markdown.markdown(text, extensions=["tables", "sane_lists"])


def build():
    d = json.loads(CARDS.read_text(encoding="utf-8"))
    voc = json.loads(VOCAB.read_text(encoding="utf-8"))

    # 卡片
    cards = []
    for b in d["books"]:
        for c in b["cards"]:
            body = c["body"]
            body = "\n".join(ln for ln in body.splitlines()
                             if not (ln.strip().startswith("*") and ln.strip().endswith("*") and len(ln.strip()) > 2))
            cards.append({"id": c["id"], "name": c["name"], "book": b["title"],
                          "guess": c["guess"], "html": md(body)})

    # 词汇（压缩字段）
    vocab = [[r["word"], r["pos_all"], r["cn"], r["book_no"], r["unit"], 1 if r["star"] else 0] for r in voc]

    payload = json.dumps({"cards": cards, "vocab": vocab,
                          "units": [{"id": u["id"], "title": u["title"], "book": u["book_short"],
                                     "unit": u["unit"], "grammar": u["grammar"]} for u in units_meta.UNITS]},
                         ensure_ascii=False)

    tpl = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>上海高中英语 · 知识图谱</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{{--ink:#1c1c1e;--sub:#6b6b70;--line:#e4e4e8;--accent:#0b6b5b;--bg:#f6f7f4;--soft:#eef4f1}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.7 -apple-system,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;display:flex;flex-direction:column;min-height:100vh}}
header{{background:#fff;border-bottom:1px solid var(--line);padding:12px 20px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}}
header h1{{font-size:17px;margin:0;color:var(--accent)}}
.stat{{color:var(--sub);font-size:12px}}
.spacer{{flex:1}}
input[type=search],select{{border:1px solid var(--line);border-radius:8px;padding:6px 10px;font-size:13px;background:#fff}}
.tabs{{display:flex;gap:6px}}
.tab{{border:1px solid var(--line);background:#fff;border-radius:8px;padding:6px 12px;font-size:13px;cursor:pointer;color:#444}}
.tab.on{{background:var(--accent);color:#fff;border-color:var(--accent)}}
main{{flex:1;display:flex;min-height:0}}
aside{{width:290px;background:#fff;border-right:1px solid var(--line);overflow:auto;padding:12px}}
.tree-book{{font-size:12px;color:var(--accent);font-weight:700;margin:12px 0 4px;padding-left:4px}}
.item{{padding:6px 8px;border-radius:8px;cursor:pointer;font-size:13px;display:flex;gap:8px;align-items:baseline}}
.item:hover{{background:var(--soft)}}
.item.on{{background:var(--soft);box-shadow:inset 3px 0 0 var(--accent)}}
.item .id{{color:var(--sub);font-size:11px;min-width:44px}}
#content{{flex:1;overflow:auto;padding:22px 26px}}
#vocab{{flex:1;overflow:auto;padding:18px 22px;display:none}}
.card{{max-width:860px;margin:0 auto;background:#fff;border:1px solid var(--line);border-radius:14px;padding:26px 30px}}
.card h2{{margin:0 0 4px;color:var(--accent);font-size:21px}}
.card h3{{margin:20px 0 6px;font-size:15px;color:#14532d;border-left:3px solid var(--accent);padding-left:8px}}
.card p,.card li{{font-size:13.6px;line-height:1.8}}
.card table{{border-collapse:collapse;width:100%;font-size:12.8px;margin:8px 0}}
.card th,.card td{{border:1px solid var(--line);padding:5px 8px;vertical-align:top}}
.card th{{background:var(--soft)}}
.card blockquote{{margin:8px 0;background:var(--soft);border-left:3px solid var(--accent);padding:6px 12px;color:#333}}
.card strong{{color:#0f3d33}}
.placeholder{{color:var(--sub);text-align:center;margin-top:80px}}
.vbar{{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:10px}}
.vstat{{font-size:13px;color:var(--sub)}}
.vtable{{width:100%;border-collapse:collapse;font-size:13px;background:#fff}}
.vtable th{{background:var(--soft);position:sticky;top:0;z-index:2;font-size:12px;color:#33584c;text-align:left;padding:6px 8px;border-bottom:1px solid #cfdcd6}}
.vtable td{{padding:5px 8px;border-bottom:1px dotted #d9d9d9;vertical-align:middle}}
.vtable tr:hover td{{background:#fafcfb}}
.w-en b{{font-family:Georgia,"Times New Roman",serif;font-size:14px}}
.pos{{color:#8a8a8a;font-size:11px}}
.bx{{display:inline-block;width:15px;height:15px;border:1px solid #9aa;border-radius:3px;margin-right:4px;cursor:pointer;vertical-align:-2px;background:#fff}}
.bx.on{{background:var(--accent);border-color:var(--accent);position:relative}}
.bx.on::after{{content:"";position:absolute;left:4px;top:1px;width:4px;height:8px;border:solid #fff;border-width:0 2px 2px 0;transform:rotate(45deg)}}
.hide-cn .cn{{visibility:hidden}}
.hide-en .w-en{{visibility:hidden}}
.tag{{font-size:10px;color:#b45309;margin-left:6px}}
footer{{border-top:1px solid var(--line);background:#fff;padding:6px 16px;font-size:12px;color:var(--sub);display:flex;gap:18px}}
#print{{display:none}}
@media print{{
  @page{{size:A4;margin:12mm 12mm}}
  body{{display:block;background:#fff}}
  header,aside,#content,#vocab,footer{{display:none!important}}
  #print{{display:block!important}}
  .pbook{{page-break-before:always}}
  .pbook:first-child{{page-break-before:auto}}
  .pbook h1{{font-size:20pt;color:#0b6b5b;margin:0 0 6mm}}
  .pcard{{page-break-before:always}}
  .pcard h2{{font-size:14pt;color:#0b6b5b;margin:0 0 2mm;border-bottom:1px solid #0b6b5b;padding-bottom:1mm}}
  .pcard h3{{font-size:10.5pt;margin:4mm 0 1mm;color:#14532d}}
  .pcard p,.pcard li{{font-size:9.2pt;line-height:1.55;margin:1mm 0}}
  .pcard table{{font-size:8.6pt;margin:2mm 0}}
  .pcard th,.pcard td{{padding:1.2mm 1.6mm}}
  .pcard blockquote{{margin:2mm 0;padding:1mm 3mm;background:#f4f7f5}}
  .pcard ul,.pcard ol{{margin:1mm 0 1mm 5mm}}
}}
</style></head>
<body>
<header>
  <h1>上海高中英语 · 知识图谱</h1>
  <span class="stat" id="stat"></span>
  <span class="spacer"></span>
  <div class="tabs">
    <button class="tab on" data-v="card">卡片</button>
    <button class="tab" data-v="vocab">词汇</button>
    <button class="tab" data-v="print">打印版</button>
  </div>
</header>
<main>
  <aside id="tree"></aside>
  <div id="content"><div class="placeholder">← 从左侧选一个单元</div></div>
  <div id="vocab">
    <div class="vbar">
      <select id="fbook"><option value="">全部册</option></select>
      <select id="funit"><option value="">全部单元</option></select>
      <select id="fstate">
        <option value="">全部状态</option>
        <option value="0">未背完</option>
        <option value="5">已背完（5 勾）</option>
      </select>
      <input type="search" id="fq" placeholder="搜索单词 / 中文">
      <button class="tab" id="hideCn">遮住中文</button>
      <button class="tab" id="hideEn">遮住英文</button>
      <button class="tab" id="random">随机抽 20 词</button>
      <span class="vstat" id="vstat"></span>
    </div>
    <table class="vtable"><thead><tr>
      <th style="width:16%">英文</th><th style="width:14%">词性</th>
      <th style="width:22%">D0 D+1 D+3 D+7 D+15</th>
      <th>中文</th><th style="width:7%">单元</th>
    </tr></thead><tbody id="vbody"></tbody></table>
  </div>
  <div id="print"></div>
</main>
<footer><span>点击左侧单元看卡片</span><span>词汇页：点方框打勾，进度存在本机浏览器</span><span id="fname"></span></footer>
<script>const DATA = {payload};</script>
<script>
const $ = s => document.querySelector(s);
const KEY = 'dsh-eng-vocab-v1';
let marks = JSON.parse(localStorage.getItem(KEY) || '{{}}');
const save = () => localStorage.setItem(KEY, JSON.stringify(marks));
const vkey = i => 'v' + i;

function buildTree(){{
  const t = $('#tree'); t.innerHTML='';
  let last='';
  DATA.cards.forEach((c,idx)=>{{
    if(c.book!==last){{ last=c.book;
      const b=document.createElement('div'); b.className='tree-book'; b.textContent=c.book; t.appendChild(b); }}
    const el=document.createElement('div'); el.className='item'; el.dataset.idx=idx;
    el.innerHTML='<span class="id">'+c.id+'</span><span>'+c.name+'</span>';
    el.onclick=()=>open(idx); t.appendChild(el);
  }});
}}
function open(idx){{
  const c=DATA.cards[idx];
  $('#content').innerHTML='<div class="card"><h2>'+c.id+'　'+c.name+'</h2>'+c.html+'</div>';
  $('#content').scrollTop=0;
  document.querySelectorAll('.item').forEach(e=>e.classList.toggle('on',+e.dataset.idx===idx));
}}
function setView(v){{
  $('#content').style.display = v==='card'?'block':'none';
  $('#vocab').style.display = v==='vocab'?'block':'none';
  $('#print').style.display = v==='print'?'block':'none';
  document.querySelectorAll('.tab[data-v]').forEach(b=>b.classList.toggle('on',b.dataset.v===v));
  if(v==='print') buildPrint();
}}
function buildPrint(){{
  if($('#print').dataset.done) return;
  let out='', last='';
  DATA.cards.forEach(c=>{{
    if(c.book!==last){{ if(last) out+='</div>'; last=c.book;
      out+='<div class="pbook"><h1>'+c.book+'</h1>'; }}
    out+='<article class="pcard"><h2>'+c.id+'　'+c.name+'</h2>'+c.html+'</article>';
  }});
  if(last) out+='</div>';
  $('#print').innerHTML=out; $('#print').dataset.done='1';
}}
// ---- 词汇 ----
const V = DATA.vocab;
function countMarks(i){{ return (marks[vkey(i)]||'').split('').filter(x=>x==='1').length; }}
function initFilters(){{
  const fb=$('#fbook'), fu=$('#funit');
  const books=[...new Set(V.map(v=>v[3]))].sort((a,b)=>a-b);
  books.forEach(b=>fb.innerHTML+='<option value="'+b+'">'+['','必修一','必修二','必修三','选必一','选必二','选必三','选必四'][b]+'</option>');
  DATA.units.forEach(u=>fu.innerHTML+='<option value="'+u.id+'">'+u.book+' U'+u.unit+' '+u.title+'</option>');
}}
function renderVocab(){{
  const b=$('#fbook').value, u=$('#funit').value, st=$('#fstate').value, q=$('#fq').value.trim().toLowerCase();
  const body=$('#vbody'); body.innerHTML='';
  let shown=0, done=0, total=0;
  V.forEach((v,i)=>{{
    total++;
    const n=countMarks(i); if(n>=5) done++;
    if(b && String(v[3])!==b) return;
    if(u && ('E-'+v[3]+'.'+v[4])!==u) return;
    if(st==='0' && n>=5) return;
    if(st==='5' && n<5) return;
    if(q && !(v[0].toLowerCase().includes(q)||v[2].includes(q))) return;
    shown++;
    const tr=document.createElement('tr');
    let boxes='';
    for(let k=0;k<5;k++){{
      const on=((marks[vkey(i)]||'')||'').padStart(5,'0')[k]==='1';
      boxes+='<span class="bx'+(on?' on':'')+'" data-i="'+i+'" data-k="'+k+'"></span>';
    }}
    tr.innerHTML='<td class="w-en"><b>'+v[0]+'</b>'+(v[5]?'<span class="tag">★</span>':'')+'</td>'+
      '<td class="pos">'+v[1]+'</td><td>'+boxes+'</td><td class="cn">'+v[2]+'</td>'+
      '<td class="pos">'+v[3]+'.'+v[4]+'</td>';
    body.appendChild(tr);
  }});
  $('#vstat').textContent='显示 '+shown+' 词 ｜ 已背完 '+done+' / '+total;
  document.querySelectorAll('.bx').forEach(el=>el.onclick=()=>{{
    const i=el.dataset.i, k=+el.dataset.k;
    let s=(marks[vkey(i)]||'').padStart(5,'0').split('');
    s[k]=s[k]==='1'?'0':'1'; marks[vkey(i)]=s.join(''); save();
    el.classList.toggle('on');
    renderVocab();
  }});
}}
$('#fbook').onchange=()=>{{ $('#funit').value=''; renderVocab(); }};
$('#funit').onchange=renderVocab; $('#fstate').onchange=renderVocab; $('#fq').oninput=renderVocab;
$('#hideCn').onclick=()=>{{ $('#vocab').classList.toggle('hide-cn'); $('#hideCn').classList.toggle('on'); }};
$('#hideEn').onclick=()=>{{ $('#vocab').classList.toggle('hide-en'); $('#hideEn').classList.toggle('on'); }};
$('#random').onclick=()=>{{
  const pool=V.map((v,i)=>({{v,i}})).filter(x=>countMarks(x.i)<5);
  pool.sort(()=>Math.random()-0.5);
  const pick=new Set(pool.slice(0,20).map(x=>x.i));
  $('#fbook').value=''; $('#funit').value=''; $('#fstate').value=''; $('#fq').value='';
  renderVocab();
  document.querySelectorAll('#vbody tr').forEach((tr,idx)=>{{}});
  const body=$('#vbody'); body.innerHTML='';
  [...pick].forEach(i=>{{ const v=V[i]; const tr=document.createElement('tr');
    tr.innerHTML='<td class="w-en"><b>'+v[0]+'</b></td><td class="pos">'+v[1]+'</td><td>随机</td><td class="cn">'+v[2]+'</td><td class="pos">'+v[3]+'.'+v[4]+'</td>';
    body.appendChild(tr); }});
  $('#vstat').textContent='随机 20 词（从未背完的词中抽）';
}};
document.querySelectorAll('.tab').forEach(b=>{{ if(b.dataset.v) b.onclick=()=>setView(b.dataset.v); }});
initFilters(); buildTree(); renderVocab();
(function(){{
  const h=location.hash;
  if(h.startsWith('#v')) setView('vocab');
  const m=h.match(/^#c=(.+)$/);
  if(m){{ const i=DATA.cards.findIndex(c=>c.id===decodeURIComponent(m[1])); if(i>=0) open(i); }}
}})();
$('#stat').textContent = DATA.cards.length + ' 个单元 · ' + V.length + ' 个词条';
$('#fname').textContent = DATA.cards.length + ' 单元 / ' + V.length + ' 词';
</script>
</body></html>"""
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(tpl, encoding="utf-8")
    print("saved", OUT, len(tpl) // 1024, "KB")


if __name__ == "__main__":
    build()
