#!/usr/bin/env python3
"""Triage every committed #437 fixture shape: recorded GitHub headings vs
the base walk and the head walk, plus the shape's `limitation` marking.

Usage: fixture_triage.py <head-scripts-dir> <base-scripts-dir> <out.json>

Classes: agree-both, fix (base wrong, head right), regress (base right,
head wrong), wrong-both. For each non-agreeing head answer it also reports
whether the recorded response HTML carries a raw `<!--` left open at the
end of the document (a crude tokenizer: `<!-->`, `<!--->`, `-->` and
`--!>` close), which is the amended acceptance 1 carve-out's condition.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURES = ("gen_toc_family_one.json", "gen_toc_comment_shapes.json",
            "gen_toc_container_walk.json")


def walk(scripts: str, pages: list) -> list:
    proc = subprocess.run([sys.executable, "-B", str(HERE / "walk_worker.py"), scripts],
                          input=json.dumps(pages).encode(), capture_output=True, check=True)
    return json.loads(proc.stdout)


def open_comment_at_end(html: str) -> bool:
    """Whether a literal `<!--` in the HTML is still open at its end."""
    at, inside = 0, False
    while True:
        if not inside:
            m = re.compile(r"<!--").search(html, at)
            if not m:
                return False
            rest = html[m.end():]
            if rest.startswith(">"):
                at = m.end() + 1
                continue
            if rest.startswith("->"):
                at = m.end() + 2
                continue
            inside, at = True, m.end()
        else:
            m = re.compile(r"--!?>").search(html, at)
            if not m:
                return True
            inside, at = False, m.end()


def main() -> int:
    head, base, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    rows = []
    for fixture in FIXTURES:
        shapes = json.loads((Path(head) / fixture).read_text())["shapes"]
        pages = [s["page"] for s in shapes]
        h, b = walk(head, pages), walk(base, pages)
        for s, ha, ba in zip(shapes, h, b):
            gh = s["headings"]
            hok, bok = ha["headings"] == gh, ba["headings"] == gh
            cls = {(True, True): "agree-both", (True, False): "fix",
                   (False, True): "regress", (False, False): "wrong-both"}[(hok, bok)]
            lim = s.get("limitation")
            rows.append({"fixture": fixture, "name": s["name"], "class": cls,
                         "github": gh, "base": ba["headings"], "head": ha["headings"],
                         "limitation": lim,
                         "lim_walk_matches_head": (lim or {}).get("walk") == ha["headings"] if lim else None,
                         "lim_base_agreed_true": (lim or {}).get("base_agreed") == bok if lim else None,
                         "open_comment_in_html": open_comment_at_end(s["response_bytes"]),
                         "page": s["page"]})
    out.write_text(json.dumps(rows, indent=1))
    from collections import Counter
    print("per fixture/class:", sorted(Counter((r["fixture"], r["class"]) for r in rows).items()))
    unmarked = [r for r in rows if not r["class"].startswith(("agree", "fix")) and not r["limitation"]]
    print("disagreeing head answers without a limitation mark:", len(unmarked))
    for r in unmarked:
        print("  UNMARKED", r["fixture"], r["name"])
    bad = [r for r in rows if r["limitation"] and not (r["lim_walk_matches_head"] and r["lim_base_agreed_true"])]
    print("limitation marks inconsistent with measured walk/base:", len(bad))
    for r in rows:
        if r["class"] == "regress":
            print("REGRESS", r["fixture"], "|", r["name"], "| dir", (r["limitation"] or {}).get("direction"),
                  "| owner", (r["limitation"] or {}).get("owner"), "| open-comment-in-html", r["open_comment_in_html"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
