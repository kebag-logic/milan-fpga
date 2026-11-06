#!/usr/bin/env python3
"""Count every planted pattern of milan_dp's explicit campaigns against its target, as each driver's own plant step does.

usage: anchor_scan.py <repo root>
Sequential edits are applied in order, because a later pattern may read an earlier replacement. Exit 1 on any miss.
"""
import importlib
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.dont_write_bytecode = True
milan = root / "tb/verilator/milan_dp"
sys.path.insert(0, str(milan))
misses = 0
total = 0


def apply(campaign, name, target, edits):
    """Apply one arm's (pattern, replacement) pairs to `target`, as the driver would."""
    global misses, total
    text = target.read_text()
    for pattern, replacement in edits:
        total += 1
        count = text.count(pattern)
        if count != 1:
            misses += 1
            print(f"MISS {campaign}: {name!r}: {count} time(s) in {target.name}: {pattern[:70]!r}")
        text = text.replace(pattern, replacement)


unb = importlib.import_module("unb_mutants")
for m in unb.MUTATIONS:
    for where in ("pp", "crf"):
        edits = [(p, r) for w, p, r in m.edits if w == where]
        if edits:
            apply("unb", m.name, (unb.PP_HDL / unb.PP_TOP) if where == "pp" else unb.CRF_RTL, edits)

gsi = importlib.import_module("gsi_mutants")
gsi_files = {"dp": gsi.DP_RTL, "pp": gsi.PP_HDL / gsi.PP_TOP, "uc": gsi.PP_HDL / gsi.PP_UCODE}
for m in gsi.MUTATIONS:
    edits = m.edits if hasattr(m, "edits") else m[1]
    for where in gsi_files:
        chosen = [(p, r) for w, p, r in edits if w == where]
        if chosen:
            apply("gsi", getattr(m, "name", m[0]), gsi_files[where], chosen)

crf = importlib.import_module("crflic_mutants")
for m in crf.MUTATIONS:
    apply("crflic", m[0], crf.DP_RTL, [(m[1], m[2])])

dyn = importlib.import_module("dynmap_mutants")
for m in dyn.MUTATIONS:
    leg, name, edits, _breaks = m[:4]
    where = m[4] if len(m) > 4 else ""
    if where.startswith("pp:"):
        target = dyn.PP_HDL / where[3:]
    else:
        target = dyn.SHADOW_RTL if where == "shadow" else dyn.DP_RTL
    apply("dynmap", name, target, edits)

ren = importlib.import_module("render_mutants")
for name, source, pattern, replacement, _mode, _breaks in ren.MUTATIONS:
    apply("render", name, ren.SOURCES[source][0], [(pattern, replacement)])

print(f"{total} planted patterns, {misses} that do not match exactly once")
sys.exit(1 if misses else 0)
