#!/usr/bin/env python3
"""Prove that round 2 left every measurement table byte-identical.

usage: tables_identity.py <repo> <base rev> <head rev> [<old PR body> <new PR body>]

A table is a maximal run of lines that start with `|`. Each table is named by
the heading above it and its order under that heading. A table whose header
row is `| Issue item | Verdict | Evidence |` or `| #606 item | Verdict |
Evidence |` is a verdict table, which round 2 was ruled to regrade (F1, S2);
every other table is a measurement table.

For each page and the PR body the script prints:
  * every table at base and head with its line count and sha256;
  * a unified diff of the base's measurement tables against the head's
    tables of the same names (it must be empty);
  * the tables that exist only at head (the saved-state tables);
  * a unified diff of the verdict tables, for the reader.
Exit 0 only when every base measurement table is byte-identical at head.
"""
import difflib
import hashlib
import subprocess
import sys
from pathlib import Path

PAGES = ["docs/findings/606_FIRST_BIND_MEASUREMENT.md", "docs/findings/608_75_WITHDRAWAL_AND_RESTART.md"]
VERDICT = ("| Issue item | Verdict | Evidence |", "| #606 item | Verdict | Evidence |")


def tables(text):
    out, heading, count, cur = [], "(top)", {}, None
    for line in text.splitlines(keepends=True):
        if line.startswith("#"):
            heading = line.strip()
        if line.startswith("|"):
            if cur is None:
                count[heading] = count.get(heading, 0) + 1
                cur = [f"{heading} / table {count[heading]}", []]
                out.append(cur)
            cur[1].append(line)
        else:
            cur = None
    return [(name, "".join(body)) for name, body in out]


def report(label, old, new):
    ok = True
    t0, t1 = dict(tables(old)), dict(tables(new))
    print(f"== {label}")
    for tag, tb in (("base", t0), ("head", t1)):
        for name, body in tb.items():
            kind = "verdict" if body.startswith(VERDICT) else "measurement"
            print(f"  {tag} {kind:11s} {len(body.splitlines()):4d} lines sha256 {hashlib.sha256(body.encode()).hexdigest()}  {name}")
    meas = [n for n, b in t0.items() if not b.startswith(VERDICT)]
    a = "".join(t0[n] for n in meas)
    b = "".join(t1.get(n, "") for n in meas)
    d = list(difflib.unified_diff(a.splitlines(keepends=True), b.splitlines(keepends=True), "base measurement tables", "head same tables"))
    print(f"  measurement tables at base: {len(meas)}; byte-identical at head: {sum(t1.get(n) == t0[n] for n in meas)}")
    print("  diff of measurement tables (empty = byte-identical):")
    sys.stdout.writelines("    " + x for x in d)
    if not d:
        print("    <empty>")
    ok &= not d and all(t1.get(n) == t0[n] for n in meas)
    added = [n for n in t1 if n not in t0]
    print(f"  tables only at head: {added or 'none'}")
    removed = [n for n in t0 if n not in t1]
    print(f"  tables only at base: {removed or 'none'}")
    ok &= not removed
    for n in t0:
        if t0[n].startswith(VERDICT):
            print(f"  verdict table diff, {n}:")
            sys.stdout.writelines("    " + x for x in difflib.unified_diff(
                t0[n].splitlines(keepends=True), t1.get(n, "").splitlines(keepends=True), "base", "head"))
    return ok


def show(repo, rev, path):
    if rev == "WORKTREE":
        return (Path(repo) / path).read_text()
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout


repo, base, head = sys.argv[1:4]
ok = True
for p in PAGES:
    ok &= report(f"{p} {base} -> {head}", show(repo, base, p), show(repo, head, p))
if len(sys.argv) == 6:
    ok &= report("PR body, round 1 -> round 2", Path(sys.argv[4]).read_text(), Path(sys.argv[5]).read_text())
print("RESULT", "PASS: every measurement table is byte-identical" if ok else "FAIL")
sys.exit(0 if ok else 1)
