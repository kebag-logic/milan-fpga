"""Classify R585-9's census-matrix rows: refused by the audit hook at run time, or by the lint alone."""
import json
import sys

HOOK = ("asks for ", " while the pin proof runs, not by the helper", "has the helper start ", "a function of the pin proof")
rows = [json.loads(ln) for ln in open(sys.argv[1], encoding="utf-8") if ln.startswith("{")]
counts = {}
for row in rows:
    found = row.get("findings") or ([row["detail"]] if "detail" in row else [])
    line = row.get("line")
    hook = [f for f in found if any(h in f for h in HOOK)
            and (line is None or int(f.split(":")[1].split()[0]) >= line)]
    kind = "clean" if row["case"] == "clean" else "hook" if hook else "lint only"
    counts[kind] = counts.get(kind, 0) + 1
    print(f"{'PASS' if row['pass'] else 'FAIL'}  {kind:9}  {row['case']}")
print(counts)
