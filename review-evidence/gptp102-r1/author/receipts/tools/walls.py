#!/usr/bin/env python3
"""Wall times of each step of one timed `make all` log (timed_make.py format).

usage: walls.py <make.log> <summary.json> [--json out.json]

Rows: the four targets of the top-level `all` (contract, tb, lint, docs), split
at their first recipe lines; each sub-make (make[1] Entering .. Leaving); inside
each sub-make that runs a mutant driver, the suite part (Entering .. the
`python3 mutants.py` line) and the driver (that line .. Leaving); the whole run.
"""
import json, re, sys

log, summary = sys.argv[1], sys.argv[2]
out_json = sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--json" else None
s = json.load(open(summary))
end = s["wall_s"]
lines = []
for raw in open(log, encoding="utf-8", errors="replace"):
    m = re.match(r"\s*([0-9.]+) (.*)", raw.rstrip("\n"))
    if m:
        lines.append((float(m.group(1)), m.group(2)))

ent = re.compile(r"make\[1\]: (Entering|Leaving) directory '.*?/(?:clone|after|gates|eq)/(.*)'")
marks = {"contract": "python3 tb/check_phc_contract.py",
         "tb": "make -C tb/verilator/ucpu",
         "lint": "verilator --lint-only",
         "docs": "python3 scripts/generate_diagrams.py --check"}
starts = {}
subs = []          # (dir, t_in, t_driver or None, t_out)
cur = None
for t, text in lines:
    m = ent.match(text)
    if m:
        kind, d = m.groups()
        if kind == "Entering":
            cur = [d, t, None]
        else:
            subs.append((cur[0], cur[1], cur[2], t))
            cur = None
        continue
    if cur is not None:
        if cur[2] is None and re.match(r"python3 mutants\.py$", text):
            cur[2] = t
        continue
    for k, v in marks.items():
        if k not in starts and text.startswith(v):
            starts[k] = t
order = ["contract", "tb", "lint", "docs"]
bounds = [starts[k] for k in order] + [end]


def hms(x):
    x = int(round(x))
    return f"{x // 3600}:{x % 3600 // 60:02d}:{x % 60:02d}"


rows = []
for i, k in enumerate(order):
    rows.append((f"target `{k}`", bounds[i], bounds[i + 1]))
    for d, a, drv, b in subs:
        if bounds[i] <= a < bounds[i + 1]:
            rows.append((f"  sub-make `{d}`", a, b))
            if drv is not None:
                rows.append((f"    suite (build + run)", a, drv))
                rows.append((f"    driver `{d}/mutants.py`", drv, b))
rows.append((f"whole `make all` (rc {s['rc']})", 0, end))
print("| step | start (s) | end (s) | wall | wall (s) | share |")
print("|---|---:|---:|---:|---:|---:|")
for name, a, b in rows:
    print(f"| {name} | {a:.0f} | {b:.0f} | {hms(b - a)} | {b - a:.1f} | {100 * (b - a) / end:.1f} % |")
if out_json:
    json.dump([{"step": n.strip(), "start": a, "end": b, "wall_s": round(b - a, 2)} for n, a, b in rows],
              open(out_json, "w"), indent=1)
