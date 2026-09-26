#!/usr/bin/env python3
"""Compare every non-test top-level definition of syn/ooc/pp_baseline.py between two commits.

usage: production_unchanged.py <repo> <old-rev> <new-rev>
Test functions (names containing 'selftest' plus the expect_refusal helper) are
reported separately; every other top-level node must be byte-identical in source.
"""
import ast, subprocess, sys

def nodes(repo, rev):
    text = subprocess.run(["git", "-C", repo, "show", f"{rev}:syn/ooc/pp_baseline.py"],
                          capture_output=True, text=True, check=True).stdout
    out = {}
    for node in ast.parse(text).body:
        name = getattr(node, "name", None) or ast.unparse(node).split("\n")[0][:60]
        out[name] = ast.get_source_segment(text, node)
    return out

repo, old, new = sys.argv[1:4]
a, b = nodes(repo, old), nodes(repo, new)
test = lambda n: "selftest" in n or n == "expect_refusal"
for name in sorted(set(a) | set(b)):
    kind = "test" if test(name) else "production"
    state = "added" if name not in a else "removed" if name not in b else \
        ("identical" if a[name] == b[name] else "CHANGED")
    print(f"{kind}\t{state}\t{name}")
