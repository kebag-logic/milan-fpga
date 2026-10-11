#!/usr/bin/env python3
"""Which finding and refusal sites of check_aecp_commands.py does its own
self-test exercise by name?

usage: python3 -I selftest_coverage.py <clean-head-export>

Builds one regex per `p.append(f"...")` / `return [f"..."]` / `raise
GateError(f"...")` site (constant text kept, every {field} a wildcard), runs
every in-memory and file mutant of the gate's own self-test, and reports for
each site whether some mutant's expected words sit in a line that site printed.
Read-only on the export: file mutants run in the gate's own temporary copies.
"""
import ast
import importlib.util
import copy
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
src_path = root / "scripts/check_aecp_commands.py"
src = src_path.read_text(encoding="utf-8")
tree = ast.parse(src)


def pattern(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return re.escape(node.value)
    if isinstance(node, ast.JoinedStr):
        return "".join(re.escape(v.value) if isinstance(v, ast.Constant) else ".*?"
                       for v in node.values)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return pattern(node.left) + pattern(node.right)
    return None


sites = []
for node in ast.walk(tree):
    if node.lineno if hasattr(node, "lineno") else False:
        pass
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
            and node.func.attr == "append" and isinstance(node.func.value, ast.Name) \
            and node.func.value.id == "p" and node.args:
        pat = pattern(node.args[0])
        if pat:
            sites.append(("finding", node.lineno, pat))
    if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call) \
            and getattr(node.exc.func, "id", "") == "GateError" and node.exc.args:
        pat = pattern(node.exc.args[0])
        if pat and node.lineno < 900:
            sites.append(("refusal", node.lineno, pat))
    if isinstance(node, ast.Return) and isinstance(node.value, ast.List) and node.value.elts:
        pat = pattern(node.value.elts[0])
        if pat and "scoreboard" in pat:
            sites.append(("finding", node.lineno, pat))

spec = importlib.util.spec_from_file_location("gate", src_path)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
base = g.load(root)
assert not g.check(base), "clean tree does not pass"
hits = {s[1]: [] for s in sites}
for what, fn, words in g.mutants():
    inp = g.Inputs(copy.deepcopy(base.table), dict(base.texts), copy.deepcopy(base.ucode))
    try:
        fn(inp)
        got = g.check(inp)
    except g.GateError as exc:
        got = [f"  (gate refused: {exc})"]
    for line in got:
        if not all(w in line for w in words):
            continue
        for kind, ln, pat in sites:
            if re.search(pat, line, re.S):
                hits[ln].append(what)
for what, fn, words in g.file_mutants():
    got = g.planted_copy(root, fn)
    for line in got:
        if not all(w in line for w in words):
            continue
        for kind, ln, pat in sites:
            if re.search(pat, line, re.S):
                hits[ln].append(what)
miss = 0
for kind, ln, pat in sorted(sites, key=lambda s: s[1]):
    tag = "COVERED" if hits[ln] else "NOT-NAMED"
    miss += not hits[ln]
    print(f"{tag}\t{kind}\tline {ln}\t{hits[ln][:1]}")
print(f"sites: {len(sites)}, covered by name: {len(sites) - miss}, not: {miss}")
