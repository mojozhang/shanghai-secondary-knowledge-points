# -*- coding: utf-8 -*-
"""用 Chrome 无头模式把打印版 HTML 打印成 PDF。"""
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
HTML = ROOT / "输出" / "_print_cards.html"
PDF = ROOT / "输出" / "上海高中英语知识图谱手册.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                "--virtual-time-budget=60000", f"--print-to-pdf={PDF}", HTML.as_uri()],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("pdf:", PDF.exists(), PDF.stat().st_size)
