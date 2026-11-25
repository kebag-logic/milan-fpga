#!/usr/bin/env python3
"""rcpt.py LABEL=GLOB ...: each LABEL's milan_dp piece receipts (cases/milan_dp__*.json) merged into one case table,
case -> (outcome, returncode, output_sha256[:16]), printed as one row per case with a column per LABEL, and each
receipt's head/tree/shard. A case a LABEL did not run shows '-'. Last column: 'same' when every LABEL that ran the
case agrees, else 'DIFFER'."""
import glob, json, sys
labels, tables = [], {}
for arg in sys.argv[1:]:
    label, pattern = arg.split("=", 1)
    labels.append(label); tables[label] = {}
    for f in sorted(glob.glob(pattern)):
        d = json.load(open(f))
        print(f"# {label}: {f.split('/')[-1]} head {d.get('head','?')[:12]} tree {str(d.get('tree','?'))[:12]} "
              f"shard {d.get('shard')}")
        for r in d["results"]:
            key = (r.get("outcome"), r.get("returncode"), (r.get("output_sha256") or "?")[:16])
            if r["case"] in tables[label]:
                sys.exit(f"{label}: {r['case']} twice")
            tables[label][r["case"]] = key
cases = []
for t in tables.values():
    cases += [c for c in t if c not in cases]
print("case".ljust(18) + "".join(l.ljust(28) for l in labels) + "verdict")
for c in cases:
    vals = [tables[l].get(c) for l in labels]
    ran = {v for v in vals if v}
    cell = lambda v: (f"{v[0]}/{v[1]}/{v[2]}" if v else "-").ljust(28)
    print(c.ljust(18) + "".join(cell(v) for v in vals) + ("same" if len(ran) == 1 else "DIFFER"))
