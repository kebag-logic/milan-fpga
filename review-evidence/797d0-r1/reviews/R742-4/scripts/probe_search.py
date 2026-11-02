#!/usr/bin/env python3
"""Plant copy forms of a recorded statement in a disposable clone and report the rows the audit generator gives.

Usage: probe_search.py <clone>. Each case writes one tracked page, renders through the clone's own generator,
reads the Findings row and the page's status, then restores the clone.
"""
import json, re, subprocess, sys
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
DATA, OUT = clone / "scripts/docs_inventory.json", clone / "docs/DOCUMENTATION_AUDIT.md"


def run(*args):
    return subprocess.run(args, cwd=clone, text=True, capture_output=True)


def restore():
    run("git", "reset", "-q", "--hard", "HEAD")
    run("git", "clean", "-qfdx")


def case(name, page, text, expect_line, statement=None):
    """Plant `text` on `page`. expect_line None means no row may appear and the page stays as it was."""
    restore()
    target = clone / page
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    run("git", "add", "-f", page)
    wrote = run("python3", "-I", "scripts/docs_inventory.py", "--write")
    audit = OUT.read_text(encoding="utf-8")
    link = re.escape(page)
    rows = [r for r in audit.splitlines() if re.match(rf"\| D0-\d+ \| \[{link}", r)]
    status = re.findall(rf"^\| \[{link}\]\([^)]*\) .*$", audit, re.M)
    state = "stale" if status and "| stale |" in status[0] else ("current" if status else "?")
    line = rows[0].split("|")[3].strip() if rows else None
    if expect_line is None:
        good = not rows and state == "current"
    else:
        good = len(rows) >= 1 and line == str(expect_line) and state == "stale"
    print(f"{'PASS' if good else 'FAIL'}\t{name}\trows={len(rows)}\tline={line}\tstatus={state}\twrite_rc={wrote.returncode}")
    return good


D1 = "The processor answers four Stream Input fields itself"  # D0-063
D2 = "All five"
results = []
P = "docs/guides/PROBE_R4.md"
H = "# Probe\n\nIntro line.\n\n"
sentence = "was deleted 2026-08-13 with this repository's own AECP/AEM engine"  # D0-024 `also`
forms = [
    ("underscore emphasis, whole", H + "_The processor answers four Stream Input fields itself._\n", 5),
    ("underscore emphasis, double, partial", H + "The __processor answers__ four _Stream Input_ fields itself.\n", 5),
    ("mixed underscore and asterisk", H + "The ***processor*** _answers_ four __Stream Input__ fields itself.\n", 5),
    ("inline link", H + "The [processor](../x.md) answers four Stream Input fields itself.\n", 5),
    ("reference link", H + "The processor answers [four Stream Input][y] fields itself.\n", 5),
    ("collapsed reference link", H + "The processor answers [four Stream Input][] fields itself.\n", 5),
    ("wrapped link", H + "The processor answers [four\nStream Input](x) fields itself.\n", 5),
    ("link in a wrapped quote", H + "> The processor answers [four\n> Stream Input](x) fields itself.\n", 5),
    ("image alt link form", H + "The processor answers ![four Stream Input](x.png) fields itself.\n", 5),
    ("closing comma", H + "The processor answers four Stream Input fields itself, and more.\n", 5),
    ("closing semicolon", H + "The processor answers four Stream Input fields itself; more.\n", 5),
    ("closing colon", H + "The processor answers four Stream Input fields itself:\n", 5),
    ("no closing punctuation", H + "The processor answers four Stream Input fields itself\n", 5),
    ("closing dash clause", H + "The processor answers four Stream Input fields itself - more.\n", 5),
    ("line further down, wrapped", H + "a\n\nb\n\nThe processor answers\nfour Stream Input fields itself.\n", 9),
    ("link above the copy keeps the line", H + "[a\nb](c) text\n\nThe processor answers four Stream Input fields itself.\n", 8),
    ("`also` sentence, a tail-carrying quote", H + "It " + sentence + ", so nothing changes.\n", 5),
    ("`also` sentence with underscore emphasis", H + "It _was deleted_ 2026-08-13 with this repository's own AECP/AEM engine.\n", 5),
]
for name, text, line in forms:
    results.append(case(name, P, text, line))
negatives = [
    ("longer word stays no copy", H + "The processor answers four Stream Input fields itselfish.\n"),
    ("inner underscore stays no copy", H + "The processor answers four Stream_Input fields itself.\n"),
    ("snake identifier stays no copy", H + "The processor answers four stream_input fields itself.\n"),
    ("break between paragraphs", H + "The processor answers four\n\nStream Input fields itself.\n"),
    ("a different number", H + "The processor answers five Stream Input fields itself.\n"),
]
for name, text in negatives:
    results.append(case(name, P, text, None))
restore()
print(f"probe_search: {sum(results)}/{len(results)} as expected")
sys.exit(0 if all(results) else 1)
