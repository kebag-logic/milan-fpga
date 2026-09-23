#!/usr/bin/env python3
"""Run base and head walks over a probe corpus, render with GitHub every
page whose two walks list different headings (plus every Nth page where
they agree, as a conformance sample), and classify each rendered page.

Usage: probe_run.py <corpus.json> <head-scripts> <base-scripts> <cache> <out.json> [N]

Classes: agree-both, fix, regress, wrong-both. A regression's page is
flagged `has_comment_opener` when its bytes carry `<!--` anywhere: a page
without one cannot fall inside acceptance 1's amended carve-out (a raw-HTML
comment the renderer leaves open).
"""
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(script: str, arg, payload) -> list:
    args = [sys.executable, "-B", str(HERE / script)] + ([arg] if isinstance(arg, str) else arg)
    proc = subprocess.run(args, input=json.dumps(payload).encode(), capture_output=True, check=False)
    if proc.returncode not in (0, 1):
        raise SystemExit(proc.stderr.decode())
    return json.loads(proc.stdout)


def main() -> int:
    corpus, head, base, cache, out = sys.argv[1:6]
    sample = int(sys.argv[6]) if len(sys.argv) > 6 else 0
    rows = json.loads(Path(corpus).read_text())
    pages = [r["page"] for r in rows]
    h, b = run("walk_worker.py", head, pages), run("walk_worker.py", base, pages)
    todo = [i for i, (x, y) in enumerate(zip(h, b))
            if x["headings"] != y["headings"] or (sample and i % sample == 0)]
    rendered = run("render.py", cache, [pages[i] for i in todo])
    result = []
    for i, rec in zip(todo, rendered):
        if rec["exit"] != 0:
            result.append({"name": rows[i]["name"], "page": pages[i], "class": "UNRENDERED",
                           "walks_differ": h[i]["headings"] != b[i]["headings"], "exit": rec["exit"],
                           "has_comment_opener": "<!--" in pages[i]})
            continue
        gh = rec["headings"]
        hok, bok = h[i]["headings"] == gh, b[i]["headings"] == gh
        cls = {(True, True): "agree-both", (True, False): "fix",
               (False, True): "regress", (False, False): "wrong-both"}[(hok, bok)]
        direction = None
        if not hok:
            extra = [x for x in h[i]["headings"] if x not in gh]
            missing = [x for x in gh if x not in h[i]["headings"]]
            direction = "+".join(k for k, v in (("escape", extra), ("withhold", missing)) if v) or "order"
        result.append({"name": rows[i]["name"], "page": pages[i], "class": cls,
                       "walks_differ": h[i]["headings"] != b[i]["headings"],
                       "github": gh, "base": b[i]["headings"], "head": h[i]["headings"],
                       "head_direction": direction, "has_comment_opener": "<!--" in pages[i],
                       "request_sha256": rec["request_sha256"], "response_sha256": rec["response_sha256"],
                       "exit": rec["exit"]})
    Path(out).write_text(json.dumps(result, indent=1))
    print("corpus pages:", len(pages), "| walks differ:", sum(r["walks_differ"] for r in result),
          "| rendered:", len(result), "| render exits nonzero:", sum(r["exit"] != 0 for r in result))
    print("classes (walks differ):", sorted(Counter(r["class"] for r in result if r["walks_differ"]).items()))
    print("classes (sample, walks equal):", sorted(Counter(r["class"] for r in result if not r["walks_differ"]).items()))
    reg = [r for r in result if r["class"] == "regress"]
    print("regressions:", len(reg), "| without any `<!--` on the page:",
          sum(not r["has_comment_opener"] for r in reg))
    print("regression directions:", sorted(Counter((r["has_comment_opener"], r["head_direction"]) for r in reg).items()))
    for r in reg:
        print("REGRESS", "comment" if r["has_comment_opener"] else "NO-COMMENT", r["head_direction"], "|", r["name"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
