# Generated from R467-1 probe_partition.py: its header and its arm B, verbatim; arms A and C dropped
# because the function they call, partition_ties, no longer exists.
#!/usr/bin/env python3
"""Mutation probe for resmap_map.py's ties (run against a disposable copy).

Usage: probe_partition.py <copy of syn/resmap/resmap_map.py>
Arm A: replace partition_ties with a stub that never fails and re-run the
self-test; if it still passes 11 of 11, no arm exercises the partition tie.
Arm B: on the self-test fixture, inflate a non-processor leaf's LUT figure in
the hierarchical report (and every ancestor's? no: the leaf only) and call
build(); if it ties clean, a wrong leaf LUT figure outside the recorded
processor scopes is absorbed as a sharing adjustment.
Arm C: prove algebraically on the fixture that partition holds whatever the
leaf LUT values are (it is an identity of the adjustment definition).
"""
import importlib.util, io, contextlib, sys, tempfile, random
from pathlib import Path
src = Path(sys.argv[1])
def load(text, name):
    p = src.with_name(name + ".py"); p.write_text(text)
    spec = importlib.util.spec_from_file_location(name, p); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); return m
orig = src.read_text()
# Arm B
m = load(orig, "resmap_map_orig")
with tempfile.TemporaryDirectory() as tmp:
    d = Path(tmp); figures, scopes = m._fixture(d)
    m._plant(d, "map_hierarchy.rpt", "|   leaf | m | 2 | 2 |", "|   leaf | m | 7 | 7 |")
    try:
        res = m.build(d, figures, scopes); print("ARM B (leaf LUT 2 -> 7, a wrong figure): TIED CLEAN; adjustment at top =", res["adjustments"]["top"]["LUT"])
    except m.TieError as e:
        print("ARM B: caught:", e)
