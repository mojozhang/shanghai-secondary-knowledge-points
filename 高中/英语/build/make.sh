#!/bin/bash
# 构建《上海高中英语》：词汇默写本（+ 后续知识图谱手册）
set -e
cd "$(dirname "$0")/.."
PY=python3
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

echo "== 1/3 生成词汇默写本 HTML =="
$PY build/gen_vocab_book.py

echo "== 2/3 检查故事词表覆盖 =="
$PY build/story_check.py

echo "== 3/3 打印词汇默写本 PDF =="
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=120000 \
  --print-to-pdf="输出/上海高中英语-词汇默写本.pdf" \
  "file://$PWD/输出/_vocab_book.html" >/dev/null 2>&1
ls -lh 输出/*.pdf
