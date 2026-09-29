#!/usr/bin/env python3
"""R391-5: every mutant in a d3_mutants.py results.json has a README row in
tb/pp_top, tb/acmp_nvm or tb/rx_validator whose last cell equals the number
of checks it failed. Usage: check_readme_counts.py <processor checkout> <results.json>"""
import json, re, sys
root, res = sys.argv[1], json.load(open(sys.argv[2]))
txt = ''.join(open(f"{root}/{f}").read() for f in
              ("tb/pp_top/README.md", "tb/acmp_nvm/README.md", "tb/rx_validator/README.md"))
bad = 0
for x in res:
    k = x["mutant"]
    if k.startswith("golden"):
        print(f"{k}: {x['verdict']}")
        continue
    m = re.search(r"^\|[^\n]*`%s`[^\n]*$" % re.escape(k), txt, re.M)
    if not m:
        print(f"NO ROW {k}"); bad += 1; continue
    cell = m.group(0).rstrip(" |").split("|")[-1].strip()
    n = len(x["failing_checks"])
    num = re.match(r"\d+", cell)
    ok = num is not None and int(num.group(0)) == n or re.search(r"\((%d) FAILs?\)" % n, m.group(0))
    print(f"{k}: {x['verdict']}, {n} failing, README '{cell[:40]}' {'OK' if ok else 'MISMATCH'}")
    bad += 0 if (ok and x["verdict"] == "KILLED") else 1
print(f"{len(res)} entries, {bad} problems")
sys.exit(1 if bad else 0)
