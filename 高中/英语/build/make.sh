#!/bin/bash
# 构建《上海高中英语》：知识图谱（PDF/HTML/Word/Excel）+ 词汇默写本（PDF）
set -e
cd "$(dirname "$0")/.."
PY=python3
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

echo "== 1/9 解析单元卡片 =="
$PY build/parse.py

echo "== 2/9 生成知识图谱 HTML =="
$PY build/gen_html.py

echo "== 3/9 生成打印版 HTML =="
$PY build/gen_print.py

echo "== 4/9 打印知识图谱 PDF =="
$PY build/gen_pdf.py

echo "== 5/9 生成 Word =="
$PY build/gen_docx.py

echo "== 6/9 生成 Excel =="
$PY build/gen_xlsx.py

echo "== 7/9 生成词汇默写本 HTML =="
$PY build/gen_vocab_book.py

echo "== 8/9 检查故事覆盖并打印默写本 PDF =="
$PY build/story_check.py
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=120000 \
  --print-to-pdf="输出/上海高中英语-词汇默写本.pdf" \
  "file://$PWD/输出/_vocab_book.html" >/dev/null 2>&1

echo "== 9/9 压缩 PDF（qpdf，无损：字体与文本层不变） =="
shrink() {
  local f="$1"
  [ -f "$f" ] || return 0
  if ! command -v qpdf >/dev/null 2>&1; then
    echo "  $(basename "$f"): 未安装 qpdf，跳过"
    return 0
  fi
  local before after
  before=$(wc -c <"$f" | tr -d ' ')
  qpdf --linearize --object-streams=generate --compress-streams=y \
       --recompress-flate --compression-level=9 "$f" "$f.tmp.pdf"
  after=$(wc -c <"$f.tmp.pdf" | tr -d ' ')
  if [ "$after" -lt "$before" ]; then
    mv "$f.tmp.pdf" "$f"
  else
    rm -f "$f.tmp.pdf"
  fi
  echo "  $(basename "$f"): $before -> $(wc -c <"$f" | tr -d ' ') bytes"
}
shrink "输出/上海高中英语知识图谱手册.pdf"
shrink "输出/上海高中英语-词汇默写本.pdf"

ls -lh 输出/*.pdf 输出/*.docx 输出/*.xlsx 输出/*.html | awk '{print $5, $9}'
