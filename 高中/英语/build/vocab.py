# -*- coding: utf-8 -*-
"""词汇数据：按单元分组、全书去重、统计。"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "词汇库.json"
sys.path.insert(0, str(ROOT / "build"))
import units_meta  # noqa: E402

BOOK_ORDER = {b["no"]: b for b in units_meta.BOOKS}


def load():
    rows = json.loads(DATA.read_text(encoding="utf-8"))
    for r in rows:
        r.setdefault("pos_all", r.get("pos", ""))
    return rows


def by_unit(rows=None):
    """{unit_id: [records...]}，单元内按课本出现顺序。"""
    rows = rows or load()
    out = {}
    for r in rows:
        out.setdefault(r["id"], []).append(r)
    return out


def master(rows=None):
    """全书去重：同一单词合并释义、词性与出现单元。"""
    rows = rows or load()
    merged = {}
    for r in rows:
        key = r["word"].lower()
        if key not in merged:
            merged[key] = {
                "word": r["word"], "pos_all": r["pos_all"], "cn": r["cn"],
                "star": r["star"], "units": [r["id"]], "book_no": r["book_no"],
                "senses": [s for s in r["cn"].split("；") if s],
            }
        else:
            m = merged[key]
            m["units"].append(r["id"])
            m["star"] = m["star"] or r["star"]
            for s in r["cn"].split("；"):
                if s and s not in m["senses"]:
                    m["senses"].append(s)
            pos = [p for p in r["pos_all"].split("/") if p]
            have = [p for p in m["pos_all"].split("/") if p]
            for p in pos:
                if p not in have:
                    have.append(p)
            m["pos_all"] = "/".join(have)
    out = list(merged.values())
    for m in out:
        m["cn"] = "；".join(m.pop("senses"))
        m["units"] = sorted(set(m["units"]), key=lambda x: (int(x.split("-")[1].split(".")[0]), int(x.split(".")[1])))
    out.sort(key=lambda x: x["word"].lower())
    return out


def stats(rows=None):
    rows = rows or load()
    u = by_unit(rows)
    return {
        "entries": len(rows),
        "unique": len(master(rows)),
        "units": len(u),
        "star": sum(1 for r in rows if r["star"]),
        "words_per_unit": {k: len(v) for k, v in u.items()},
    }


if __name__ == "__main__":
    s = stats()
    print(s["entries"], "entries,", s["unique"], "unique,", s["units"], "units,",
          s["star"], "starred")
    for k, v in s["words_per_unit"].items():
        print(k, v)
