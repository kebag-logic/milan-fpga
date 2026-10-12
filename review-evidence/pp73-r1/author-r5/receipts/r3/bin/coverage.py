#!/usr/bin/env python3
"""pkg_coverage.py TREE: R608-1's selftest_coverage.py, over the package.

Every finding site (an f-string or string starting with two spaces that a
check appends or returns) and every refusal site (raise GateError) in
scripts/aecp_gate/ outside the self-test's own modules becomes a regex (the
constant text kept, every {field} a wildcard). Every plant of the self-test is
run - in memory, in a file copy, and the generator alone - and a site counts as
covered by name when some plant's output line carries all of that plant's
words AND matches the site. Read-only on TREE."""
import ast
import copy
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.dont_write_bytecode = True
sys.path.insert(0, str(root / "scripts"))
from aecp_gate import gate, inputs, plants, selftest, field_plants, fields  # noqa: E402

SKIP = ("plants.py", "field_plants.py", "selftest.py", "__init__.py")


def pattern(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return re.escape(node.value)
    if isinstance(node, ast.JoinedStr):
        return "".join(re.escape(v.value) if isinstance(v, ast.Constant) else ".*?"
                       for v in node.values)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        a, b = pattern(node.left), pattern(node.right)
        return a + b if a is not None and b is not None else None
    return None


def text0(node):
    if isinstance(node, ast.Constant):
        return node.value if isinstance(node.value, str) else ""
    if isinstance(node, ast.JoinedStr) and node.values and isinstance(node.values[0], ast.Constant):
        return node.values[0].value
    return ""


sites = []
for f in sorted((root / "scripts/aecp_gate").glob("*.py")):
    if f.name in SKIP:
        continue
    for node in ast.walk(ast.parse(f.read_text())):
        cands = []
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr == "append" and node.args:
            cands.append(("finding", node.args[0]))
        if isinstance(node, ast.ListComp):
            cands.append(("finding", node.elt))
        if isinstance(node, ast.List):
            cands += [("finding", e) for e in node.elts]
        if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call) \
                and getattr(node.exc.func, "id", "") == "GateError" and node.exc.args:
            cands.append(("refusal", node.exc.args[0]))
        for kind, arg in cands:
            if kind == "finding" and not re.match(r"  [\w.]+:", text0(arg)):
                continue
            pat = pattern(arg)
            if pat:
                sites.append((kind, f"{f.name}:{arg.lineno}", pat))

base = inputs.load(root)
assert not gate.check(base), "clean tree does not pass"
runs = []
for what, fn, words in plants.MUTANTS + field_plants.MUTANTS:
    runs.append((what, words, selftest.in_memory(base, fn)))
for what, fn, words in selftest.OBSERVED_MUTANTS:
    runs.append((what, words, selftest.on_copy(base, fn)))
for what, fn, words in selftest.FILE_MUTANTS:
    runs.append((what, words, selftest.planted_copy(root, fn)))
for entry in fields.registry(base):
    if entry['status'] == 'held':
        probe = entry['probe']
        fn = lambda inp, p=probe: fields.plant_field(inp, p)
        runs.append((entry['path'], probe['words'], selftest.in_memory(base, fn)))
hits = {s[1]: [] for s in sites}
for what, words, got in runs:
    for line in got:
        if not all(w in line for w in words):
            continue
        for kind, at, pat in sites:
            if re.search(pat, line, re.S):
                hits[at].append(what)
miss = 0
for kind, at, pat in sites:
    miss += not hits[at]
    print(f"{'COVERED' if hits[at] else 'NOT-NAMED'}\t{kind}\t{at}\t{hits[at][:1]}")
print(f"sites: {len(sites)} ({sum(k == 'finding' for k, _, _ in sites)} findings, "
      f"{sum(k == 'refusal' for k, _, _ in sites)} refusals), covered by name: "
      f"{len(sites) - miss}, not: {miss}; plants run: {len(runs)} "
      f"(+{len(selftest.GENERATOR_MUTANTS)} generator-alone plants, whose refusals are gen_ucode.py's)")
