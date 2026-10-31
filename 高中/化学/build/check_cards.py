# -*- coding: utf-8 -*-
"""校验知识卡结构：章节顺序、例题数、自评答案、易错边界、禁用写法。"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REQ = ["**⚡ 先猜**", "### 30 秒概述", "### 30 秒自评", "### 🔑 原理与方程式",
       "**适用条件**", "**易错边界**", "### 例题 1 · L1 基础", "### 例题 2 · L2 常考",
       "### 例题 3 · L3 综合", "### ⏱️ 限时挑战", "### ✅ 接下来做什么"]

def main():
    bad = 0
    for f in sorted(ROOT.glob("[0-9][0-9]-*.md")):
        s = f.read_text(encoding="utf-8")
        if not s.startswith("# "):
            print(f, "缺一级标题"); bad += 1
        cards = re.split(r"^## ([A-E]-\d+\.\d+) (.+)$", s, flags=re.M)
        n = (len(cards) - 1) // 3
        if n < 3:
            print(f, f"考点数 {n} < 3"); bad += 1
        for i in range(1, len(cards), 3):
            cid, body = cards[i], cards[i+2]
            pos = [body.find(k) for k in REQ]
            if any(p < 0 for p in pos):
                miss = [REQ[j] for j, p in enumerate(pos) if p < 0]
                print(f, cid, "缺段落:", miss); bad += 1
            elif pos != sorted(pos):
                print(f, cid, "段落顺序错"); bad += 1
            if body.count("> **答案**") < 1:
                print(f, cid, "自评无答案"); bad += 1
            if len(re.findall(r"^\d\. ", body.split("**易错边界**")[-1].split("###")[0], re.M)) < 3:
                print(f, cid, "易错边界不足 3 条"); bad += 1
            for k in ["**解析**", "**💥 陷阱**", "**变式**"]:
                if body.count(k) < 3:
                    print(f, cid, f"{k} 少于 3 处"); bad += 1
        for pat, name in [(r"\$", "LaTeX $"), (r"!\[", "图片"), (r"<[a-z]+>", "HTML 标签")]:
            if re.search(pat, s):
                print(f, "含", name); bad += 1
        eq = s.split("## 📐 方程式速查")[-1].split("## ")[0] if "## 📐 方程式速查" in s else ""
        rows = [l for l in eq.splitlines() if l.startswith("| (") or re.match(r"^\| \(\d+-\d+\)", l)]
        rel = s.split("## 🕸️ 考点关系")[-1] if "## 🕸️ 考点关系" in s else ""
        rel_rows = [l for l in rel.splitlines() if re.match(r"^\| [A-E]-\d", l)]
        print(f"{f.name}: {n} 考点, {len(rows)} 方程式, {len(rel_rows)} 关系")
        if len(rows) < 6:
            print("  方程式 <6 条"); bad += 1
        if len(rel_rows) < 6:
            print("  关系 <6 条"); bad += 1
    print("问题数:", bad)
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
