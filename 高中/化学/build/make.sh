#!/bin/bash
# 一键重建全部交付物：MD → 校验 → JSON → Excel / Word / HTML / PDF
set -e
cd "$(dirname "$0")/.."

PY=python3
DOCX_PY=/Users/mojozhang/.dsh/dsh-runtimes/dsh-primary-runtime/dependencies/python/bin/python3

echo "== 1/7 校验知识卡结构 =="
$PY build/check_cards.py

echo "== 2/7 解析 Markdown =="
$PY build/parse.py

echo "== 3/7 生成 Excel =="
$DOCX_PY build/gen_xlsx.py

echo "== 4/7 生成 Word =="
DSH_SKIP_PDF=1 $DOCX_PY build/gen_docx.py

echo "== 5/7 生成 HTML 图谱 =="
$PY build/gen_html.py

echo "== 6/7 打印 PDF（Chrome，与网页一致）=="
$PY build/gen_pdf.py

echo "== 7/7 压缩 PDF（qpdf，无损）=="
if command -v qpdf >/dev/null 2>&1; then
  f="输出/上海高中化学知识图谱手册.pdf"
  before=$(wc -c <"$f" | tr -d ' ')
  qpdf --linearize --object-streams=generate --compress-streams=y \
       --recompress-flate --compression-level=9 "$f" "$f.tmp.pdf"
  after=$(wc -c <"$f.tmp.pdf" | tr -d ' ')
  if [ "$after" -lt "$before" ]; then mv "$f.tmp.pdf" "$f"; else rm -f "$f.tmp.pdf"; fi
  echo "  $(basename "$f"): $before -> $(wc -c <"$f" | tr -d ' ') bytes"
else
  echo "  未安装 qpdf，跳过"
fi

echo
echo "输出目录："
ls -lh 输出/
