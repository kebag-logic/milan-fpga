#!/usr/bin/env python3
"""Show which clause ids docs/traceability/gen_module_matrix.py's clause_refs()
takes from the IEEE 802.1Q SRP-10 traceability row at each commit, using the
generator's own regex and its first-three cap, read from the generator source.

usage: python3 matrix_clause_probe.py <repo> <commit> [<commit> ...]
"""
import re
import subprocess
import sys

repo = sys.argv[1]


def show(commit, path):
    return subprocess.run(["git", "-C", repo, "show", f"{commit}:{path}"],
                          check=True, capture_output=True, text=True).stdout


for commit in sys.argv[2:]:
    gen = show(commit, "docs/traceability/gen_module_matrix.py")
    pat = re.search(r'clause_re = re\.compile\(r"([^"]+)"\)', gen).group(1)
    cap = re.search(r"update\(cls\[:(\d+)\]\)", gen).group(1)
    clause_re = re.compile(pat)
    row = next(ln for ln in show(commit, "docs/traceability/ieee8021q.md").splitlines()
               if ln.startswith("| SRP-10 |"))
    cls = clause_re.findall(row)
    mods = sorted(set(re.findall(r"`([A-Za-z0-9_]+)`", row)))
    print(f"{commit[:8]} regex={pat!r} cap={cap}")
    print(f"  SRP-10 clause tokens in order: {cls[:8]}")
    print(f"  kept (first {cap}): {cls[:int(cap)]}")
    print(f"  modules named in the row: {mods}")
    for tok in cls[:int(cap)]:
        i = row.find(tok)
        print(f"    {tok!r} matched in ...{row[max(0, i - 25):i + len(tok) + 10]!r}...")
