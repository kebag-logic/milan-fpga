#!/usr/bin/env python3
"""Each hosted worker's projected seconds (the tree's dealer) against its measured suite windows.

usage: python3 -I deal_check.py TREE RUN_LOGDIR [RUN_LOGDIR...]
RUN_LOGDIR holds <n>.log, `gh run view --log --job` of Verilator shard n/19. For every worker
prints projected total (overhead + its pieces' figures), measured (overhead + windows, from the
tree's own measure_log), and per suite: figure, measured window, ratio.
"""
from __future__ import annotations

import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "scripts"))
import suite_shards as s  # noqa: E402

suites = s.expand_suites(s.sweep_suites(tree / "tb/verilator"))
owners, load = s.balance(suites, 19)
for logdir in map(Path, sys.argv[2:]):
    print(f"== {logdir}")
    print(f"{'w':>2} {'proj':>6} {'meas':>6} {'m/p':>5}  suites (figure -> measured)")
    for n in range(19):
        log = logdir / f"{n}.log"
        if not log.exists():
            continue
        t = s.measure_log(log.read_text(encoding="utf-8"))
        mine = [x for x in suites if owners[x] == n]
        meas = (t.overhead or 0) + sum(t.seconds.values())
        big = [f"{x} {s.SUITE_SECONDS[x]}->{t.seconds.get(x, '?')}" for x in mine
               if s.SUITE_SECONDS[x] >= 200 or t.seconds.get(x, 0) >= 200]
        print(f"{n:>2} {load[n]:6} {meas:6} {meas / load[n]:5.2f}  ovh {s.WORKER_OVERHEAD_SECONDS[n]}->{t.overhead}; "
              + "; ".join(big))
