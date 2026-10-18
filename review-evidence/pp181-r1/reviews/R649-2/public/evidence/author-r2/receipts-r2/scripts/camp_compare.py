#!/usr/bin/env python3
"""Compare base and head campaign records (issue #181 evidence, round 2).

Per-mutant logs are compared on their graded lines only (PASS, FAIL, KILLED,
SURVIVED, check tallies, verdicts); build output and temp names are not records.

For each campaign: its console log as a sorted set of lines, and every text record
(.log .json .txt .out) in its output directory outside build trees, after
normalizing the tree, output and scratch paths. Prints IDENTICAL or the differences.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path("<data>/tmp/pp181-a635/r2/camp")
CAMPS = ["d3", "notify", "dispatch", "aecp", "ctr", "gsi", "name_wr", "acmp",
         "name_state", "elab_guards"]
SUBS = [(re.compile(r"<data>/tmp/pp181-a635/r2/base-tree"), "TREE"),
        (re.compile(r"<data>/lanes/pp181-cut"), "TREE"),
        (re.compile(r"<data>/tmp/pp181-a635/r2/camp/[A-Za-z0-9_.-]+"), "OUT"),
        (re.compile(r"<data>/tmp/pp181-a635/tmp/[A-Za-z0-9_.-]+"), "TMP"),
        (re.compile(r"(/tmp/|tmp/)[A-Za-z0-9_]+-[a-z0-9_]{8}\b"), "TMP"),
        (re.compile(r"\b\d+(\.\d+)?\s*s\b"), "Ns"),
        (re.compile(r"\(\d+(\.\d+)?s\)"), "(Ns)")]
BUILD = ("obj_dir", "obj_", "tree", "work", "copy", "hdl", "tb")


def norm(text):
    for rx, rep in SUBS:
        text = rx.sub(rep, text)
    return text


def records(d):
    out = {}
    for p in sorted(d.rglob("*")):
        if not p.is_file() or p.suffix not in (".log", ".json", ".txt", ".out"):
            continue
        rel = p.relative_to(d)
        if any(part.startswith(BUILD) for part in rel.parts[:-1]):
            continue
        if p.name == "results.json":
            # parallel jobs finish in any order: compare the mutants keyed by name
            data = json.loads(p.read_text())
            if isinstance(data, list):
                data = sorted(data, key=lambda r: json.dumps(r, sort_keys=True))
                for r in data:
                    if isinstance(r, dict):
                        for k in [k for k in r if re.search(r"sec|time|dur", k)]:
                            r.pop(k)
            out[str(rel)] = norm(json.dumps(data, sort_keys=True, indent=1))
            continue
        graded = [l for l in p.read_text(errors="replace").splitlines()
                  if re.search(r"PASS|FAIL|KILLED|SURVIVED|checks?:|verdict", l)
                  and not re.search(r"^(make|verilator|g\+\+|ccache|-|%)", l.strip())]
        out[str(rel)] = norm("\n".join(graded))
    return out


A = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "base")
B = ROOT / (sys.argv[2] if len(sys.argv) > 2 else "head")
bad = 0
for c in CAMPS:
    b, h = A / c, B / c
    lb = sorted(norm((A / f"{c}.log").read_text()).splitlines())
    lh = sorted(norm((B / f"{c}.log").read_text()).splitlines())
    rb, rh = records(b), records(h)
    diffs = [k for k in sorted(set(rb) | set(rh)) if rb.get(k) != rh.get(k)]
    same_console = lb == lh
    print(f"{c}: console {'IDENTICAL' if same_console else 'DIFFERS'}; "
          f"{len(rb)} base / {len(rh)} head records, {len(diffs)} differ")
    for k in diffs[:12]:
        print(f"    differs: {k}")
    if not same_console:
        sb, sh = set(lb), set(lh)
        for l in sorted(sb - sh)[:6]:
            print(f"    base only: {l[:150]}")
        for l in sorted(sh - sb)[:6]:
            print(f"    head only: {l[:150]}")
    bad += (not same_console) + len(diffs)
sys.exit(1 if bad else 0)
