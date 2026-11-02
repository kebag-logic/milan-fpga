#!/usr/bin/env python3
"""usage: fails.py <trace jsonl> [n]  Scratch only: print each failing cleanup's timeline."""
import json, sys
tr = [json.loads(l) for l in open(sys.argv[1])]
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 99
for t in [t for t in tr if t["outcome"] != "clean"][:limit]:
    print(f"--- owner {t['owner']} root {t['root']} notified {t['notified']} load {t['load']} elapsed {t['elapsed']} resumed {t['resumed']}")
    print("    sent:", t["sent"])
    for at, took, st in t["passes"]:
        print(f"    pass@{at:6.3f} took {took:5.3f}: " + "; ".join(f"{p} {v[0]} {v[1]} ppid {v[2]} {v[3]}" if v else f"{p} gone" for p, v in st.items()))
