"""Largest media_phase figure each worker count accepts under the checker's 1620 s rule."""
import sys
sys.path.insert(0, sys.argv[1])
import suite_shards as s
suites = s.expand_suites(s.sweep_suites(s.SUITE_ROOT))
for workers in (16, 17):
    best = None
    for figure in range(900, 2001):
        _, load = s.balance(suites, workers, {**s.SUITE_SECONDS, "media_phase": figure}, (122,) * workers)
        if max(load[:-1]) <= 1620:
            best = figure
    print(f"{workers} workers at 45 min: largest media_phase figure accepted {best} s")
for figure in (1364, 1400, 1488):
    _, load = s.balance(suites, 17, {**s.SUITE_SECONDS, "media_phase": figure}, (122,) * 17)
    print(f"  17 workers, figure {figure} s: busiest regular worker {max(load[:-1])} s")
