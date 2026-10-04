#!/usr/bin/env python3
"""List every ID use at a tree that check-ids.py passes only through a lenient form
(family prefix, or trailing numeric segment read as minus n), and cross-check the
gate with an independent naive scan (every [PT]-UPPER token vs the first-column rows).

usage: ids_forms.py <repo>
"""
import importlib.util
import re
import sys
from pathlib import Path

repo = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("ci", repo / "scripts/check-ids.py")
ci = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ci)
params = ci.defined_ids(ci.table_section((repo / ci.PARAMS).read_text(),
                        "## 7. Parameter master table (F01.5)", "F01.5"), "P-", "F01.5")
timing = ci.defined_ids(ci.table_section((repo / ci.TIMING).read_text(),
                        '<a id="fig-08-constants"></a>', "F08.1"), "T-", "F08.1")
rows = set(params) | set(timing)
lenient = {}
for rel in ci.scanned_files(repo):
    data = (repo / rel).read_bytes()
    if b"\0" in data[:8192]:
        continue
    text = data.decode("utf-8", errors="replace")
    for line, token, kind in ci.uses(text):
        table = params if token.startswith("P-") else timing
        if kind == "family" or (token not in table and ci.resolves(token, kind, set(table))):
            lenient.setdefault((kind, token), []).append(f"{rel}:{line}")
print(f"rows: F01.5 {len(params)}, F08.1 {len(timing)}")
for (kind, token), where in sorted(lenient.items()):
    print(f"LENIENT {kind:6} {token:28} {len(where):3} uses, e.g. {', '.join(where[:3])}")
# naive independent scan: any [PT]-<UPPER> run, longest hyphenated, no lookbehind tricks
naive = re.compile(r"\b([PT]-[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*)")
odd = {}
for rel in ci.scanned_files(repo):
    data = (repo / rel).read_bytes()
    if b"\0" in data[:8192]:
        continue
    for m in naive.finditer(data.decode("utf-8", errors="replace")):
        tok = m.group(1)
        if tok in rows or tok in ci.REGISTRY_WORDS:
            continue
        line = data[:m.start()].count(b"\n") + 1 if False else None
        odd.setdefault(tok, []).append(str(rel))
print(f"naive tokens without an exact row: {len(odd)}")
for tok, where in sorted(odd.items()):
    print(f"NAIVE {tok:30} {len(where):3} in {', '.join(sorted(set(where))[:4])}")
