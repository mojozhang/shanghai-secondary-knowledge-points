#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""纯文本公式 → LaTeX（MathJax 可渲染），统一处理 Unicode 上下标、希腊字母、组合重音。

设计原则：
1. 源文件写"人看着舒服"的形式（v₀、x²、√(2h/g)、v̄）；
2. 转换器负责映射成标准 LaTeX，不留任何非 ASCII 字符；
3. 映射不到的字符一律降级为原样文本，绝不输出半截公式。
"""
import hashlib
import pathlib
import re

try:                     # 渲染时才需要，未安装则走"只读缓存"模式
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt  # noqa: E402
    _HAS_MPL = True
except Exception:        # pragma: no cover
    plt = None
    _HAS_MPL = False

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT / "图" / "公式"

# ---------- 字符映射表 ----------
GREEK = {
    "α": r"\alpha", "β": r"\beta", "γ": r"\gamma", "δ": r"\delta",
    "ε": r"\varepsilon", "ζ": r"\zeta", "η": r"\eta", "θ": r"\theta",
    "ι": r"\iota", "κ": r"\kappa", "λ": r"\lambda", "μ": r"\mu",
    "ν": r"\nu", "ξ": r"\xi", "ο": "o", "π": r"\pi", "ρ": r"\rho",
    "σ": r"\sigma", "τ": r"\tau", "υ": r"\upsilon", "φ": r"\varphi",
    "χ": r"\chi", "ψ": r"\psi", "ω": r"\omega",
    "Γ": r"\Gamma", "Δ": r"\Delta", "Θ": r"\Theta", "Λ": r"\Lambda",
    "Ξ": r"\Xi", "Π": r"\Pi", "Σ": r"\Sigma", "Υ": r"\Upsilon",
    "Φ": r"\Phi", "Ψ": r"\Psi", "Ω": r"\Omega",
}

SYMBOLS = {
    "×": r"\times", "÷": r"\div", "·": r"\cdot", "−": "-", "–": "-",
    "≈": r"\approx", "≠": r"\neq", "≤": r"\leq", "≥": r"\geq",
    "→": r"\to", "⇒": r"\Rightarrow", "⇔": r"\Leftrightarrow",
    "∝": r"\propto", "∞": r"\infty", "±": r"\pm", "∓": r"\mp",
    "∠": r"\angle", "⊥": r"\perp", "∥": r"\parallel", "△": r"\triangle",
    "∁": r"\complement", "∈": r"\in", "∉": r"\notin", "∪": r"\cup", "∩": r"\cap",
    "⊆": r"\subseteq", "⊂": r"\subset", "⊇": r"\supseteq",
    "∅": r"\emptyset", "∀": r"\forall", "∃": r"\exists",
    "ℝ": r"\mathbb{R}", "ℕ": r"\mathbb{N}", "ℤ": r"\mathbb{Z}",
    "ℚ": r"\mathbb{Q}", "ℂ": r"\mathbb{C}",
    "∵": r"\because", "∴": r"\therefore", "⌒": r"\frown",
    "∽": r"\backsim", "≌": r"\cong", "≡": r"\equiv",

    "°": r"^{\circ}", "℃": r"^{\circ}\mathrm{C}", "%": r"\%",
    "′": "'", "″": "''",
    "∑": r"\sum", "∫": r"\int", "∂": r"\partial",
    "≪": r"\ll", "≫": r"\gg", "⇄": r"\rightleftharpoons",
    "⇌": r"\rightleftharpoons", "≡": r"\equiv", "∛": r"\sqrt[3]", "∜": r"\sqrt[4]",
}

SUP = {
    "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
    "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
    "⁺": "+", "⁻": "-", "ⁿ": "n", "ⁱ": "i",
    "ᵃ": "a", "ᵇ": "b", "ᶜ": "c", "ᵈ": "d", "ᵉ": "e", "ᶠ": "f", "ᵍ": "g",
    "ʰ": "h", "ʲ": "j", "ᵏ": "k", "ˡ": "l", "ᵐ": "m", "ᵒ": "o", "ᵖ": "p",
    "ʳ": "r", "ˢ": "s", "ᵗ": "t", "ᵘ": "u", "ᵛ": "v", "ʷ": "w", "ˣ": "x",
    "ʸ": "y", "ᶻ": "z",
    "²": "2", "³": "3", "¹": "1",       # U+00B2/B3/B9
}
SUB = {
    "₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4",
    "₅": "5", "₆": "6", "₇": "7", "₈": "8", "₉": "9",
    "₊": "+", "₋": "-", "ₐ": "a", "ₑ": "e", "ₒ": "o",
    "ₓ": "x", "ₙ": "n", "ₖ": "k", "ₘ": "m", "ₚ": "p", "ᵤ": "U",
}

BASE = r"A-Za-z0-9\)\]\{\}α-ωΑ-Ω∁"
SUB_CHARS = "".join(SUB)
SUP_CHARS = "".join(SUP)


def _readable(s: str) -> bool:
    """是否只含可转换字符（不含中文等）。"""
    for c in s:
        if ord(c) < 128 or c in " \t":
            continue
        if c in GREEK or c in SYMBOLS or c in SUB or c in SUP:
            continue
        if c in "√∛∜½¼¾\u20d7":
            continue
        if 0x0300 <= ord(c) <= 0x036F:
            continue
        return False
    return True


def to_latex(s: str) -> str:
    s = s.strip()

    # 0. 源文件里的 { } 是集合花括号，先转义成字面量，避免被 LaTeX 当成分组
    s = s.replace("{", r"\{").replace("}", r"\}")

    # 0.5 向量箭头：a⃗ → \vec{a}，AB⃗ → \vec{AB}
    s = re.sub(r"(?<![A-Za-z0-9])([A-Za-z0-9]{1,2})\u20d7", lambda m: r"\vec{" + m.group(1) + "}", s)
    s = re.sub(r"([A-Za-z0-9])\u20d7", lambda m: r"\vec{" + m.group(1) + "}", s)

    # 1. 组合重音：v̄ → \bar{v}
    s = re.sub(r"([A-Za-zα-ωΑ-Ω])\u0304", lambda m: r"\bar{" + m.group(1) + "}", s)
    s = re.sub(r"([A-Za-zα-ωΑ-Ω])\u0305", lambda m: r"\overline{" + m.group(1) + "}", s)
    s = re.sub(r"([A-Za-zα-ωΑ-Ω])\u0307", lambda m: r"\dot{" + m.group(1) + "}", s)
    s = re.sub(r"([A-Za-zα-ωΑ-Ω])\u0308", lambda m: r"\ddot{" + m.group(1) + "}", s)

    # 2. 常用分数
    s = s.replace("½", r"\frac{1}{2}").replace("¼", r"\frac{1}{4}").replace("¾", r"\frac{3}{4}")

    # 2.5 指数位置的分式：a^(m/n) → a^{\frac{m}{n}}，b^(-1/3) → b^{\frac{-1}{3}}
    s = re.sub(r"\^\(\s*([^()/]{1,12})\s*/\s*([^()]{1,12})\s*\)",
               lambda m: r"^{\frac{%s}{%s}}" % (m.group(1), m.group(2)), s)
    s = re.sub(r"\^\(([^()]{1,24})\)", lambda m: "^{" + m.group(1) + "}", s)

    # 3. 根号
    RAD = {"√": "", "∛": "[3]", "∜": "[4]"}
    out, i = [], 0
    while i < len(s):
        if s[i] in RAD:
            j = i + 1
            if j < len(s) and s[j] in "([{":
                open_ch = s[j]
                close_ch = {"(": ")", "[": "]", "{": "}"}[open_ch]
                depth, k = 0, j
                while k < len(s):
                    if s[k] == open_ch:
                        depth += 1
                    elif s[k] == close_ch:
                        depth -= 1
                        if depth == 0:
                            break
                    k += 1
                out.append(r"\sqrt" + RAD[s[i]] + "{" + to_latex(s[j + 1:k]) + "}")
                i = k + 1
                continue
            m2 = re.match(r"[A-Za-z0-9.]+|[" + "".join(GREEK) + r"]", s[j:])
            arg = m2.group(0) if m2 else ""
            out.append(r"\sqrt" + RAD[s[i]] + "{" + arg + "}")
            i = j + len(arg) if arg else j
            continue
        out.append(s[i])
        i += 1
    s = "".join(out)

    # 4. 下标（含下划线写法与 Unicode 下标）
    KNOWN = {"max", "min", "avg", "tot", "net", "eq", "cm", "ab", "bc", "ac", "cd"}

    def _sub(m):
        base, word = m.group(1), m.group(2)
        w = word if word in KNOWN else word[0]
        return base + "_{" + w + "}" + word[len(w):]

    s = re.sub(r"([" + BASE + r"])_([A-Za-z0-9]+)", _sub, s)
    s = re.sub(r"([" + BASE + r"])([" + SUB_CHARS + r"]+)",
               lambda m: m.group(1) + "_{" + "".join(SUB[c] for c in m.group(2)) + "}", s)

    # 5. 上标
    s = re.sub(r"([" + BASE + r"])([" + SUP_CHARS + r"]+)",
               lambda m: m.group(1) + "^{" + "".join(SUP[c] for c in m.group(2)) + "}", s)

    # 6. 希腊字母与符号
    for k in sorted(GREEK, key=len, reverse=True):
        s = s.replace(k, GREEK[k] + " ")
    for k in sorted(SYMBOLS, key=len, reverse=True):
        s = s.replace(k, SYMBOLS[k] + " ")

    # 6.5 合并相邻上下标（v_H₂ 曾被拆成 v_{H}_{2}）
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"_\{([^{}]*)\}_\{([^{}]*)\}", r"_{\1\2}", s)
        s = re.sub(r"\^\{([^{}]*)\}\^\{([^{}]*)\}", r"^{\1\2}", s)

    # 6.8 数与函数名之间的空格转成细空隙：45°cos → 45^\circ\,cos
    s = re.sub(r"(?<=[0-9A-Za-z\)\}\]°α-ωΑ-Ω])\s+(?=(?:sin|cos|tan|cot|sec|csc|log|ln|lg)\b)", r"\\,", s)

    # 7. 函数名正体
    for fn in ["sin", "cos", "tan", "cot", "sec", "csc", "arcsin", "arccos", "arctan",
               "max", "min", "ln", "lg", "log", "exp", "lim", "sup", "inf"]:
        s = re.sub(r"(?<![\\A-Za-z])" + fn + r"(?![A-Za-z])", lambda m: r"\mathrm{" + m.group(0) + "}", s)
    # 函数名与自变量之间加细空隙：sin 210°、cos α（紧跟括号时不加）
    s = re.sub(r"(\\mathrm\{(?:sin|cos|tan|cot|sec|csc|arcsin|arccos|arctan|log|ln|lg)\})\s?"
               r"(?=[0-9A-Za-z" + "".join(GREEK) + r"]|\\[A-Za-z])", r"\1\\,", s)

    s = re.sub(r"\s+", " ", s).strip()
    # 兜底：仍残留的上下标字符（前面没有基底）→ 空基底上标
    for c, v in SUP.items():
        s = s.replace(c, "{}^" + v)
    for c, v in SUB.items():
        s = s.replace(c, "{}_" + v)

    # 片段被截断时可能以 ^ 或 _ 开头（无基底），补一个空基底
    if s.startswith("^") or s.startswith("_"):
        s = "{}" + s
    return s


def is_formula(s: str) -> bool:
    s = s.strip()
    if not s or len(s) > 60:
        return False
    if not _readable(s):
        return False
    if not re.search(r"[A-Za-z" + "".join(GREEK) + r"]", s):
        return False
    if not re.search(r"[=≈∝≤≥√+\-−×÷/]", s):
        return False
    return True


def needs_render(s: str) -> bool:
    """含根号/上下标/分数/组合重音/下划线的公式值得单独渲染。"""
    return any(c in s for c in "√²³⁰¹⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉_^½\u20d7∥⊥")


SPAN_RE = re.compile(
    "[" + SUP_CHARS + SUB_CHARS +
    r"A-Za-z0-9α-ωΑ-Ω√∝=+\-−×÷/()\[\].,·_{}½¼¾|^ \t"
    r"≤≥≈≠<>→⇒⇔∈∉∪∩⊆⊂⊇∅∀∃ℝℕℤℚℂ⌒∽≌∴∵∧∨%°′≪≫⇄∛∜∥⊥:\u0300-\u036f\u20d7]{2,}")


def spans(text: str, whole: bool = False):
    """在中文句子中找出可渲染的公式片段，返回 [(start, end, formula)]。"""
    out = []
    for m in SPAN_RE.finditer(text):
        raw = m.group(0)
        if not any(k in raw for k in "=√∝≪≫≈∈∪∩⊆⊂≥≤≠→⇒∧∨<>∥⊥"):
            continue
        if not re.search(r"[A-Za-z" + "".join(GREEK) + r"]", raw):
            continue
        if not whole and not needs_render(raw):
            continue
        a, b = m.start(), m.end()
        while a < b and text[a] in " \t":
            a += 1
        while b > a and text[b - 1] in " \t":
            b -= 1
        raw = text[a:b]
        lead = len(raw) - len(raw.lstrip(" \t-−·,;:"))
        trail = len(raw) - len(raw.rstrip(" \t-−·,;:"))
        a, b = a + lead, b - trail
        # 不要吞掉列表序号（"1. " / "- "），否则 Markdown 认不出列表
        mm = re.match(r"^(?:\d+[.)]|[-•])\s+", text[a:b])
        if mm:
            a += mm.end()
        frag = text[a:b]
        if not frag or any(ch in frag for ch in "，。\n"):
            continue
        # 末尾若是运算符（常因后面紧跟 **加粗** 而截断），回退到运算符之前
        while frag and frag[-1] in "=+−-/\\×÷^_ ":
            b -= 1
            frag = text[a:b]
        if not frag or not _readable(frag):
            continue
        # 括号不配对（例如被中文逗号截断的集合{x | x > 0，x∈R}）不转公式，避免 MathJax 报错
        if frag.count("{") != frag.count("}") or frag.count("(") != frag.count(")"):
            continue
        if not any(k in frag for k in "=√∝≪≫≈∈∪∩⊆⊂≥≤≠→⇒∧∨<>∥⊥"):
            continue
        out.append((a, b, frag))
    return out


def render(formula: str, fontsize: float = 13.0):
    """返回 (png_path, width_cm, height_cm)；失败返回 None。"""
    if "\n" in formula or "$" in formula:
        return None
    latex = to_latex(formula)
    key = hashlib.md5((latex + "|" + str(fontsize)).encode()).hexdigest()[:16]
    CACHE.mkdir(parents=True, exist_ok=True)
    png = CACHE / f"{key}.png"
    if png.exists():
        from PIL import Image
        w, h = Image.open(png).size
        return png, w / 400 * 2.54, h / 400 * 2.54
    if not _HAS_MPL:
        return None
    try:
        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, f"${latex}$", fontsize=fontsize, color="black")
        fig.savefig(png, dpi=400, transparent=True,
                    bbox_inches="tight", pad_inches=0.02)
        plt.close(fig)
    except Exception:
        try:
            plt.close(fig)
        except Exception:
            pass
        return None
    from PIL import Image
    w, h = Image.open(png).size
    return png, w / 400 * 2.54, h / 400 * 2.54


if __name__ == "__main__":
    for t in ["v̄ = Δx/Δt", "v̄ = (v₀ + v)/2", "v² − v₀² = 2ax",
              "Φ = BS", "ΣF = ma", "ν = c/λ", "θ = 30°"]:
        print(f"{t:22s} → {to_latex(t)}")
