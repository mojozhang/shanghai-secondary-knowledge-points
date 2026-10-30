#!/bin/bash
# 构建《上海高中英语》：知识图谱（PDF/HTML/Word/Excel）+ 词汇默写本（PDF）
set -e
cd "$(dirname "$0")/.."
PY=python3
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

echo "== 1/8 解析单元卡片 =="
$PY build/parse.py

echo "== 2/8 生成知识图谱 HTML =="
$PY build/gen_html.py

echo "== 3/8 生成打印版 HTML =="
$PY build/gen_print.py

echo "== 4/8 打印知识图谱 PDF =="
$PY build/gen_pdf.py

echo "== 5/8 生成 Word =="
$PY build/gen_docx.py

echo "== 6/8 生成 Excel =="
$PY build/gen_xlsx.py

echo "== 7/8 生成词汇默写本 HTML =="
$PY build/gen_vocab_book.py

echo "== 8/8 检查故事覆盖并打印默写本 PDF =="
$PY build/story_check.py
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=120000 \
  --print-to-pdf="输出/上海高中英语-词汇默写本.pdf" \
  "file://$PWD/输出/_vocab_book.html" >/dev/null 2>&1

ls -lh 输出/*.pdf 输出/*.docx 输出/*.xlsx 输出/*.html | awk '{print $5, $9}'
