#!/usr/bin/env python3
"""Judge the M2 and M6 lane routes quoted in MARK_II_AREA_PLAN.md against both route-1x1 records.

Usage: python3 -I record_vs_lane_routes.py <repo> <old-record-rev> <head-rev>

Reads the plan tables at <head-rev>, the route-1x1 entry at both revisions, and applies the
gate's own verdict_for() (syn/ooc/pp_resource_gate.py from the clean checkout at <head-rev>) to every gated figure the
plan quotes, plus the BRAM-tile ceiling derived from RAMB36 + RAMB18/2. DSP is not quoted in
the plan tables; it is reported as not quoted. Also checks that each quoted base route equals
the old record in every quoted gated figure.
"""
import json, re, subprocess, sys, pathlib

repo, old_rev, head = sys.argv[1:4]
git = lambda *a: subprocess.check_output(["git", "-C", repo, *a], text=True)

# The gate is imported from the checkout, which must be clean at <head-rev>.
assert git("rev-parse", "HEAD").strip() == git("rev-parse", head).strip(), "checkout is not at head"
assert git("status", "--porcelain", "--", "syn/ooc") == "", "syn/ooc is not clean"
sys.path.insert(0, str(pathlib.Path(repo, "syn/ooc")))
import pp_resource_gate as gate

plan = git("show", f"{head}:docs/design/MARK_II_AREA_PLAN.md").splitlines()
num = lambda s: float(s.replace(",", "").replace("+", ""))
rows = {}
for i, line in enumerate(plan, 1):
    m = re.match(r"\| (Base route at dev `e8454e27`|M2 route at `4177835c`|M6 route at `930340145`) \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \| (\d+) / (\d+) \| ([+-][\d.]+) / ([+-][\d.]+) \|", line)
    if m:
        figs = dict(zip(("LUT", "FF", "SLICE", "RAMB36", "RAMB18", "WNS_ns", "WHS_ns"), map(num, m.groups()[1:])))
        figs["BRAM_TILE"] = figs["RAMB36"] + figs["RAMB18"] / 2
        rows.setdefault(m.group(1), []).append((i, figs))

status = 0
for label, rev in (("#645/#647 record (old)", old_rev), ("#696 record (head)", head)):
    entry = json.loads(git("show", f"{rev}:syn/ooc/pp_resource_baseline.json"))["endpoints"]["route-1x1"]
    base = entry["record"]["figures"]
    print(f"== {label} at {rev[:8]}: {json.dumps(base)}")
    for name, occurrences in rows.items():
        for line, figs in occurrences:
            bad = []
            for f in gate.GATED["route"]:
                if f not in figs:
                    print(f"   {name} (plan:{line}) {f}: not quoted in the plan table")
                    continue
                verdict, ok = gate.verdict_for(entry, f, base[f], figs[f])
                if not ok:
                    bad.append(f"{f} {verdict}")
            for f, ceiling in entry.get("ceiling", {}).items():
                if figs[f] > ceiling:
                    bad.append(f"{f} exceeds ceiling {ceiling}")
            eq = all(figs[f] == base[f] for f in gate.GATED["route"] if f in figs)
            print(f"   {name} (plan:{line}): {'PASS' if not bad else 'FAIL ' + '; '.join(bad)}; equals record in quoted gated figures: {eq}")
            if bad:
                status = 1
sys.exit(status)
