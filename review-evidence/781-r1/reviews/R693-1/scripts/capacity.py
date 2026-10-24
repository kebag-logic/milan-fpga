"""Independent capacity arithmetic for media_phase at 16 and 17 workers, from the head's own selector tables.
usage: python3 -I capacity.py <repo>"""
import sys; sys.path.insert(0, sys.argv[1] + "/scripts")
import suite_shards as s
units = s.expand_suites(s.sweep_suites(sys.argv[1] + "/tb/verilator"))
ded = list(s.DEDICATED_SUITES)
reg = [u for u in units if u not in ded]
print("units", len(units), "dedicated", ded, "regular", len(reg))
for mp in (900, 1364, 1400, 1498, 1499):
    sec = dict(s.SUITE_SECONDS); sec["media_phase"] = mp
    demand = sum(sec[u] for u in reg)
    for n in (16, 17):
        cap = (n - len(ded)) * (1620 - 122)
        _, load = s.balance(units, n, sec, (122,) * n)
        worst = max(load[:-len(ded)])
        print(f"media_phase={mp:4} workers={n} regular demand={demand} capacity={cap} slack={cap - demand:5} greedy busiest regular={worst} {'fits' if worst <= 1620 else 'OVER'} dedicated={load[-1]}")
