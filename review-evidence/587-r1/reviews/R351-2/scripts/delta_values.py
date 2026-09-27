#!/usr/bin/env python3
"""Prove the round-2 commit changed no figure except the normalized-Verilog digest.

Usage: delta_values.py REPO OLD NEW
1. Page: every numeric table row at OLD reappears at NEW with identical numeric cells, same count and order.
2. Page: multiset of number tokens outside code spans; report additions and removals.
3. Input manifest: parsed JSON equal after removing export_comparison.{normalized_verilog_sha256,normalization}.
4. Every other file under docs/findings is byte-identical between OLD and NEW.
"""
import json, re, subprocess, sys
from collections import Counter
repo, old, new = sys.argv[1:4]
def show(rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout
page = "docs/findings/PP_SHADOW_BASELINE.md"
num = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?")
def cells(line):
    parts = [c.strip() for c in line.strip().strip("|").split("|")]
    return tuple(c for c in parts[1:] if num.fullmatch(c))
rows = {}
for rev in (old, new):
    rows[rev] = [cells(l) for l in show(rev, page).splitlines() if l.startswith("|") and cells(l)]
print(f"numeric table rows: old={len(rows[old])} new={len(rows[new])} identical_in_order={rows[old] == rows[new]}")
def tokens(rev):
    text = re.sub(r"`[^`]*`", "", show(rev, page))
    text = re.sub(r"\]\([^)]*\)", "]", text)  # link targets carry comment ids, not figures
    return Counter(num.findall(text))
to, tn = tokens(old), tokens(new)
added, removed = tn - to, to - tn
print("number tokens added outside code spans:", dict(sorted(added.items())) or "none")
print("number tokens removed outside code spans:", dict(sorted(removed.items())) or "none")
jpath = "docs/findings/PP_SHADOW_BASELINE_50MHZ_INPUTS.json"
jo, jn = json.loads(show(old, jpath)), json.loads(show(new, jpath))
changed = {k: (jo["export_comparison"].get(k), jn["export_comparison"].get(k))
           for k in set(jo["export_comparison"]) | set(jn["export_comparison"])
           if jo["export_comparison"].get(k) != jn["export_comparison"].get(k)}
for d in (jo, jn):
    for k in ("normalized_verilog_sha256", "normalization"):
        d["export_comparison"].pop(k, None)
print("manifest keys changed:", sorted(changed))
print("manifest equal after removing those keys:", jo == jn)
names = subprocess.run(["git", "-C", repo, "diff", "--name-only", old, new], capture_output=True, text=True, check=True).stdout.split()
print("files changed:", names)
ok = rows[old] == rows[new] and not removed and jo == jn and sorted(changed) == ["normalization", "normalized_verilog_sha256"]
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
