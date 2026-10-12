#!/usr/bin/env python3
"""Cross-run variance: per-suite windows of a second hosted run against the
head's SUITE_SECONDS, and the new split re-predicted with that run's figures
where it measured them.

Usage: python3 -I variance.py HEAD_SELECTOR REDERIVE_PY LOG...
"""
import importlib.util
import math
import sys
from pathlib import Path


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv):
    hs = load(argv[1], "head_selector")
    rd = load(argv[2], "rederive")
    other = {}
    for log in argv[3:]:
        shard, windows, ovh, *_ = rd.parse(log)
        for suite, (d, verdict) in windows.items():
            if verdict == "PASS":
                other[suite] = math.ceil(d)
        print(f"worker {shard[1]}/{shard[2]}: {len(windows)} windows, overhead "
              f"{'cut off' if ovh is None else math.ceil(ovh)}")
    table = hs.SUITE_SECONDS
    rows = sorted(((other[s] / table[s], s) for s in other if table[s] >= 60), reverse=True)
    print("suite: table s, other-run s, ratio (suites >= 60 s in the table)")
    for ratio, s in rows:
        print(f"  {s}: {table[s]} {other[s]} {ratio:.3f}")
    inv = sorted(table)
    owners, base = hs.balance(inv, 5)
    mixed = {**table, **{s: v for s, v in other.items() if s in table}}
    load2 = list(hs.WORKER_OVERHEAD_SECONDS)
    for s in inv:
        load2[owners[s]] += mixed[s]
    print(f"head split predicted (table): {base}")
    print(f"head split with the other run's windows where measured (same owners): {load2}")
    print(f"bound {hs.bound_seconds(120)} s; suites without an other-run window: "
          f"{sorted(set(inv) - set(other))}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
