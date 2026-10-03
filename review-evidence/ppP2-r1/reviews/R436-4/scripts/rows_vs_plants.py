#!/usr/bin/env python3
"""Compare the head's gate rows (tb/nvm_port/deadline_rows.py DRAIN_PLANTS) with
R436-3's plants_drain.py: every Z plant's (old, new) pairs byte-identical.
usage: rows_vs_plants.py <head export tb/nvm_port> <plants_drain.py>"""
import importlib.util, sys
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    argv = sys.argv; sys.argv = [path, "list"]
    try:
        spec.loader.exec_module(m)
    except SystemExit:
        pass
    sys.argv = argv
    return m
rows = load("dr", sys.argv[1] + "/deadline_rows.py")
src = open(sys.argv[2]).read()
ns = {}
exec(src.split("def main")[0], ns)
mine = ns["PLANTS"]
gate = dict(rows.DRAIN_PLANTS)
bad = 0
for k, v in mine.items():
    ok = k in gate and [tuple(p) for p in gate[k]] == [tuple(p) for p in v]
    bad += not ok
    print(f"{k:5} {'IDENTICAL' if ok else 'DIFFERS'}")
print("DRAIN_ON_FUZZ:", rows.DRAIN_ON_FUZZ)
print(f"{len(mine)} R436-3 plants, {bad} differ")
sys.exit(1 if bad else 0)
