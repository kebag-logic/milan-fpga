"""Summarize aecp_mutants.py results.json files: caught/escaped per plant."""
import json
import sys

for path in sys.argv[1:]:
    rows = json.load(open(path, encoding="utf-8"))
    caught = sum(1 for r in rows if r["caught"])
    print(f"{path.split('/')[-2]}: {caught}/{len(rows)} caught")
    for r in rows:
        tests = ";".join(t for t, _ in r["checks"])
        print("  ", "CAUGHT" if r["caught"] else "ESCAPED", r["name"], r["path"], tests)
