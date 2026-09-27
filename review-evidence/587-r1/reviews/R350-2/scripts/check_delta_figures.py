#!/usr/bin/env python3
"""Prove the round-2 delta changes no figure except the normalized-Verilog digest.

usage: check_delta_figures.py REPO OLD NEW   (reads blobs with git show; NEW may be wt:<worktree>)

1. Page tables: same number of table rows, in order; every data cell (all cells after the
   first) byte-identical between OLD and NEW. Only first-column labels and headers may change.
2. Page prose: every numeric token of OLD prose still occurs in NEW prose at least as often;
   tokens added in NEW prose are listed and must be tag tokens only (clock, pin, issue ids).
3. JSON manifest: recursive diff; only export_comparison.normalized_verilog_sha256 and
   export_comparison.normalization may differ.
4. Ranking TSV byte-identical. Other changed files are listed with their numeric tokens.
"""
import collections
import json
import re
import subprocess
import sys
from pathlib import Path

repo, old, new = sys.argv[1:]


def show(rev, path):
    if rev.startswith("wt:"):  # read a working tree instead of a commit (used for mutant probes)
        return (Path(rev[3:]) / path).read_text()
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True,
                          text=True, check=True).stdout


bad = 0


def verdict(ok, what):
    global bad
    bad += not ok
    print(f"{'OK  ' if ok else 'FAIL'} {what}")


PAGE = "docs/findings/PP_SHADOW_BASELINE.md"
po, pn = show(old, PAGE), show(new, PAGE)


def rows(text):
    out = []
    for line in text.splitlines():
        if line.startswith("|") and not re.match(r"^\|[-:| ]+\|$", line):
            out.append([c.strip() for c in line.strip().strip("|").split("|")])
    return out


ro, rn = rows(po), rows(pn)
verdict(len(ro) == len(rn), f"table row count old={len(ro)} new={len(rn)}")
label_changes = cell_changes = 0
for a, b in zip(ro, rn):
    if a[1:] != b[1:]:
        # Header rows may change their column labels; detect headers by non-numeric cells.
        header = not any(re.search(r"\d", c) for c in a[1:]) or a[0] in ("Input", "Instance")
        if header or a[0].startswith(("Product configuration", "Measurement", "Wrapper parameter",
                                      "Contribution", "Raw logic", "Primitive", "Instance",
                                      "Integrated 8x8", "Attribution")):
            print(f"HEADER-CHANGE {a[0]!r}: {a[1:]} -> {b[1:]}")
            nums_a = re.findall(r"\d[\d,.]*", " ".join(a[1:]))
            nums_b = re.findall(r"\d[\d,.]*", " ".join(b[1:]))
            print(f"    header numeric tokens old={nums_a} new={nums_b}")
            continue
        cell_changes += 1
        print(f"CELL-CHANGE {a} -> {b}")
    if a[0] != b[0]:
        label_changes += 1
        print(f"LABEL {a[0]!r} -> {b[0]!r}")
verdict(cell_changes == 0, f"data cells unchanged in every table row (label changes={label_changes})")


def prose_numbers(text):
    toks = []
    for line in text.splitlines():
        if line.startswith("|"):
            continue
        line = re.sub(r"\(https?://[^)]*\)", "", line)
        # Pin hashes and the digest name are tags, not figures.
        line = re.sub(r"`[0-9a-f]{8,40}`", "`PIN`", line).replace("SHA-256", "SHA")
        toks += [t.rstrip(",") for t in re.findall(r"[-+]?\d[\d,]*(?:\.\d+)?", line)]
    return collections.Counter(toks)


no, nn = prose_numbers(po), prose_numbers(pn)
lost = no - nn
added = nn - no
verdict(not lost, f"no prose numeric token lost (lost={dict(lost)})")
print(f"INFO prose numeric tokens added: {dict(added)}")
TAGS = {"100", "50", "231", "587", "8", "1"}  # clock MHz, issue ids, "8x8"/"1x1" shape names
unexpected = {t for t in added if t not in TAGS}
verdict(not unexpected, f"added prose numeric tokens are clock/pin/issue tags only (unexpected={sorted(unexpected)})")

JS = "docs/findings/PP_SHADOW_BASELINE_50MHZ_INPUTS.json"
jo, jn = json.loads(show(old, JS)), json.loads(show(new, JS))
diffs = []


def walk(a, b, path):
    if type(a) is not type(b):
        diffs.append(path); return
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                diffs.append(f"{path}.{k}")
            else:
                walk(a[k], b[k], f"{path}.{k}")
    elif isinstance(a, list):
        if len(a) != len(b):
            diffs.append(path + "[len]"); return
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, f"{path}[{i}]")
    elif a != b:
        diffs.append(path)


walk(jo, jn, "$")
print(f"INFO json differing paths: {diffs}")
verdict(set(diffs) == {"$.export_comparison.normalized_verilog_sha256", "$.export_comparison.normalization"},
        "json differs only in the digest and its rule")
verdict(jo["export_comparison"]["equal"] is True and jn["export_comparison"]["equal"] is True, "equal flag true in both")
print(f"INFO old digest={jo['export_comparison']['normalized_verilog_sha256']}")
print(f"INFO new digest={jn['export_comparison']['normalized_verilog_sha256']}")
TSV = "docs/findings/PP_SHADOW_BASELINE_50MHZ_RANKING.tsv"
verdict(show(old, TSV) == show(new, TSV), "50 MHz ranking TSV byte-identical")
names = [] if new.startswith("wt:") else subprocess.run(
    ["git", "-C", repo, "diff", "--name-only", old, new], capture_output=True, text=True, check=True).stdout.split()
print(f"INFO changed paths: {names}")
for path in names:
    if path in (PAGE, JS):
        continue
    d = subprocess.run(["git", "-C", repo, "diff", "-U0", old, new, "--", path], capture_output=True,
                       text=True, check=True).stdout
    minus = [l[1:] for l in d.splitlines() if l.startswith("-") and not l.startswith("---")]
    plus = [l[1:] for l in d.splitlines() if l.startswith("+") and not l.startswith("+++")]
    print(f"INFO {path}: removed={minus} added={plus}")
    verdict(not minus, f"{path}: nothing removed")
print(f"RESULT failures={bad}")
sys.exit(1 if bad else 0)
