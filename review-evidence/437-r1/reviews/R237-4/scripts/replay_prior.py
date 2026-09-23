#!/usr/bin/env python3
"""Replay every page the prior public review rounds recorded with a GitHub
rendering, under the base walk, the previous head's walk and this head's walk.

Usage: replay_prior.py <evidence-dir> <base> <prev> <head> <out.json>

<evidence-dir> holds files fetched from the public evidence commit
ccc7b2b199469035ccea5e534584e691b59c1234 under review-evidence/437-r1/.
The recorded rendering is each round's own (re-rendering is not repeated
here except where this round's cache already holds the page).
"""
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def walk(scripts: str, pages: list) -> list:
    p = subprocess.run([sys.executable, "-B", str(HERE / "walk_worker.py"), scripts],
                       input=json.dumps(pages).encode(), capture_output=True, check=True)
    return [a["headings"] for a in json.loads(p.stdout)]


def rows(ev: Path) -> list:
    out = []
    r3 = ev / "reviews/R237-3/receipts"
    for m in ("minimal", "minimal2"):
        pages = json.loads((r3 / f"pages/{m}.json").read_text())
        rend = json.loads((r3 / f"{m}.rendered.json").read_text())
        out += [("R237-3 " + m, n, pages[n], rend[n]["headings"]) for n in pages if n in rend]
    for m, sample in (("fuzz1", "fuzz_full_sample"), ("fuzz_core", "fuzz_core_sample")):
        pages = json.loads((r3 / f"pages/{sample}.json").read_text())
        rend = json.loads((r3 / f"{m}.json").read_text())
        out += [("R237-3 " + m, n, pages[n], rend[n]["rendered"]) for n in rend if n in pages]
    r8 = ev / "reviews/R238-2/probes"
    for f in ("batch1", "batch2", "batch3", "batch4_prior", "fuzz_seed238_complete",
              "matrix_base_vs_head", "fuzz_seed4372_no35_complete"):
        for i, line in enumerate((r8 / f"{f}.jsonl").read_text().splitlines()):
            if line.strip():
                x = json.loads(line)
                if x.get("exit", 0) == 0:
                    out.append(("R238-2 " + f, x.get("name", f"{f}#{i}"), x["page"], x["github"]))
    r2 = ev / "reviews/R237-2/receipts"
    for f in ("comment-rule-render", "regression-seed-render", "combinatorial-render"):
        for x in json.loads((r2 / f"{f}.json").read_text())["rows"]:
            out.append(("R237-2 " + f, x["name"], x["page"], x["rendered"]))
    return out


def main() -> int:
    ev, base, prev, head, dest = Path(sys.argv[1]), *sys.argv[2:6]
    rs = rows(ev)
    pages = [r[2] for r in rs]
    b, p, h = walk(base, pages), walk(prev, pages), walk(head, pages)
    table = []
    for (src, name, page, gh), bb, pp, hh in zip(rs, b, p, h):
        cls = {(True, True): "agree-both", (True, False): "fix", (False, True): "regress",
               (False, False): "wrong-both"}[(hh == gh, bb == gh)]
        table.append({"source": src, "name": name, "page": page, "github": gh, "base": bb, "prev": pp,
                      "head": hh, "class": cls, "prev_agrees": pp == gh,
                      "head_escape": any(x not in gh for x in hh), "has_comment_opener": "<!--" in page})
    Path(dest).write_text(json.dumps(table, indent=1))
    print("recorded pages replayed:", len(table))
    for src in sorted({t["source"] for t in table}):
        c = Counter(t["class"] for t in table if t["source"] == src)
        print(f"  {src:36} {dict(sorted(c.items()))}")
    reg = [t for t in table if t["class"] == "regress"]
    print("regressions vs base at this head:", len(reg), "| escape:", sum(t["head_escape"] for t in reg),
          "| pages without `<!--`:", sum(not t["has_comment_opener"] for t in reg))
    return 0


if __name__ == "__main__":
    sys.exit(main())
