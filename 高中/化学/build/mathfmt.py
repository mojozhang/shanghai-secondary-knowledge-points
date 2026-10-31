# -*- coding: utf-8 -*-
"""化学卷占位实现：不使用 LaTeX，公式与方程式一律用 Unicode 纯文本。

保留与物理卷相同的接口（spans / render / to_latex / is_formula），
这样 gen_html.py / gen_docx.py 无需改动即可直接复用。
"""


def spans(text, whole=False):
    return []


def render(frag):
    return ""


def to_latex(s):
    return s


def is_formula(s):
    return False
