"""Which locked distribution packages are not in the dependency closure of the derived apt requests?

usage: lock_roots.py <dpkg-deps.tsv from the image> <sources.lock.json> <tool-inventory.json>
"""
import json, re, sys
deps, provides = {}, {}
for line in open(sys.argv[1]):
    pkg, d, pre, prov = (line.rstrip("\n").split("\t") + ["", "", ""])[:4]
    names = []
    for clause in (d + "," + pre).split(","):
        alts = [re.split(r"[ (:]", a.strip())[0] for a in clause.split("|") if a.strip()]
        if alts: names.append(alts)
    deps[pkg] = names
    for p in prov.split(","):
        p = re.split(r"[ (]", p.strip())[0]
        if p: provides.setdefault(p, []).append(pkg)
lock = json.load(open(sys.argv[2])); inv = json.load(open(sys.argv[3]))
locked = {p["tool"] for p in lock["packages"]}
roots = sorted({t["tool"] for t in inv["tools"] if t["kind"] == "apt"})
seen, todo = set(), list(roots)
while todo:
    p = todo.pop()
    if p in seen: continue
    seen.add(p)
    for alts in deps.get(p, []):
        cands = [a for a in alts if a in deps] + [x for a in alts for x in provides.get(a, [])]
        todo.extend(cands[:1] or [])
extra = sorted(locked - seen)
# roots among the extras: not depended on by any other extra
dependents = {x for p in extra for alts in deps.get(p, []) for x in alts}
print("derived apt roots:", len(roots), "closure in lock:", len(locked & seen), "locked:", len(locked))
print("locked but outside the derived closure:", len(extra))
print("top-level extras (no other extra depends on them):", [p for p in extra if p not in dependents])
