#!/usr/bin/env python3
"""d3_union.py <d3_mutants.py> <part1.log> <part2.log>: reconcile a two-part d3 campaign against the driver's own
arm list (imported), printing every arm once with its part and verdict, and the goldens of each part."""
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("d3m", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
names = [x.name for x in m.MUTANTS]
def verdicts(path):
    out = {}
    for line in open(path):
        if line.startswith('{"mutant"'):
            d = json.loads(line); out[d["mutant"]] = d["verdict"]
    return out
p1, p2 = verdicts(sys.argv[2]), verdicts(sys.argv[3])
rows, bad = [], 0
for n in names:
    parts = [p for p, v in (("part1", p1), ("part2", p2)) if n in v]
    v = [p1.get(n), p2.get(n)]
    verdict = next((x for x in v if x), None)
    ok = len(parts) == 1 and verdict == "KILLED"
    bad += not ok
    rows.append(f"{n}\t{','.join(parts) or 'MISSING'}\t{verdict}")
g1 = {k: v for k, v in p1.items() if k.startswith("golden")}
g2 = {k: v for k, v in p2.items() if k.startswith("golden")}
print(f"driver arms: {len(names)}; part 1 verdicts: {sum(n in p1 for n in names)}; part 2 verdicts: {sum(n in p2 for n in names)}")
print(f"goldens part 1: {g1}")
print(f"goldens part 2: {g2}")
print("\n".join(rows))
gold_ok = all(v == "PASS" for v in list(g1.values()) + list(g2.values())) and g1 and g2
print(f"UNION: {len(names) - bad} of {len(names)} arms KILLED exactly once; goldens {'PASS' if gold_ok else 'NOT ALL PASS'}")
sys.exit(0 if bad == 0 and gold_ok else 1)
