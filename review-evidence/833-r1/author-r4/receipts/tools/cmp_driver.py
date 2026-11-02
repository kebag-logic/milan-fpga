#!/usr/bin/env python3
"""usage: cmp_driver.py NEW_SUMMARY OLD_SUMMARY  (one line per entry: expectation, result now, result in the old run)"""
import json, sys
rows = json.load(open(sys.argv[1]))
old = {r["name"]: r for r in json.load(open(sys.argv[2]))}
for r in rows:
    o = old.get(r["name"])
    print(f"{r['name']:45} {r['test']:9} expect={r['expect']:5} got={r['got']:5} rc={r['rc']:3} {r['seconds']:6} "
          f"old={o['got'] if o else '-'} | {r['last'][:110]}")
