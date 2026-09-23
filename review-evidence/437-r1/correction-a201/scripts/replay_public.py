#!/usr/bin/env python3
"""Replay every public rendered page of R237-3 and R238-2 (and the prior
findings R237-3 collected) under the base, the reviewed head and the working
tree. A walk agrees when it lists the headings GitHub rendered, compared by
level and first word (inline markup inside a heading is not the question)."""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import walks

PUB = Path(__file__).resolve().parent.parent / "scratch" / "public"
BASE, PREV = "574c29fa111c74e5e5ed63e4670aff1f492e28e2", "e4906bfca65c61e7e109e3532ac1b2dd5b4c0096"


def rows():
    r7 = PUB / "R237-3"
    for pages, rendered in [("pages/minimal.json", "minimal.json"),
                            ("pages/minimal2.json", "minimal2.json"),
                            ("pages/fuzz_full_sample.json", "fuzz1.json"),
                            ("pages/fuzz_core_sample.json", "fuzz_core.json"),
                            ("pages/r28_distinguishing.json", "r28_survivor.rendered.json")]:
        pg = json.loads((r7 / pages).read_text())
        rd = json.loads((r7 / rendered).read_text())
        for name, page in pg.items():
            if name in rd:
                gh = rd[name].get("rendered", rd[name].get("headings"))
                yield f"R237-3 {rendered}", name, page, gh
    for name, row in json.loads((r7 / "prior_findings.json").read_text())["rows"].items():
        gh = row["github"]
        gh = [[2, h] if isinstance(h, str) else h for h in gh]
        yield "R237-3 prior_findings", name, row["page"], gh
    for f in sorted((PUB / "R238-2").glob("*.jsonl")):
        for n, line in enumerate(f.read_text().splitlines()):
            row = json.loads(line)
            yield f"R238-2 {f.name}", row.get("name", f"{f.stem}#{n}"), row["page"], row["github"]


def key(heads):
    return [(h[0], (h[1].split() or [""])[0]) for h in heads]


def main():
    seen, data = set(), []
    for src, name, page, gh in rows():
        if page in seen:
            continue
        seen.add(page)
        data.append((src, name, page, gh))
    pages = [d[2] for d in data]
    res = {rev: walks.walk(rev, pages) for rev in (BASE, PREV, "work")}
    out = []
    for i, (src, name, page, gh) in enumerate(data):
        g = key(gh)
        verdict = {}
        for rev, tag in ((BASE, "base"), (PREV, "prev"), ("work", "work")):
            w = key(res[rev][i]["headings"])
            if w == g:
                verdict[tag] = "AGREE"
            elif set(w) > set(g):
                verdict[tag] = "ESCAPE"
            elif set(w) < set(g):
                verdict[tag] = "WITHHOLD"
            else:
                verdict[tag] = "MIXED"
            verdict[tag + "_list"] = [h[1] for h in res[rev][i]["headings"]]
        out.append({"source": src, "name": name, "page": page, "github": [h[1] for h in gh], **verdict})
    Path(sys.argv[1]).write_text(json.dumps(out, indent=1))
    c = Counter()
    for r in out:
        cls = ("regression" if r["base"] == "AGREE" and r["work"] != "AGREE" else
               "fix" if r["base"] != "AGREE" and r["work"] == "AGREE" else
               "agree" if r["work"] == "AGREE" else "both-wrong")
        r["class"] = cls
        c[cls] += 1
    Path(sys.argv[1]).write_text(json.dumps(out, indent=1))
    print(len(out), "unique pages", dict(c))
    print("vs reviewed head:", dict(Counter((r["prev"] == "AGREE", r["work"] == "AGREE") for r in out)))


if __name__ == "__main__":
    main()
