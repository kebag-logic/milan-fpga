#!/usr/bin/env python3
"""Merge batched `tb/srp_top/mutants.py --only` stdouts: arms, controls, assertion coverage.
The coverage set is the driver's own (main(), unbatched runs only), recomputed over the
union of KILLED arms' tags. usage: srp_top_merge.py names.txt batch.stdout..."""
import re, sys
names = [l.strip() for l in open(sys.argv[1]) if l.strip()]
killed, unproven, controls, covered = {}, [], {}, set()
for path in sys.argv[2:]:
    for line in open(path):
        m = re.match(r"control (\S+) ?(\S*): rc=\d+ (PASS|FAIL)", line)
        if m:
            controls.setdefault((m[1], m[2]), []).append(m[3]); continue
        m = re.match(r"(\S+): rc=\d+ failures=\d+ (KILLED|UNPROVEN) tags=(.*)", line)
        if m:
            if m[2] == "KILLED":
                killed[m[1]] = killed.get(m[1], 0) + 1
                covered.update(t.strip() for t in m[3].split(","))
            else:
                unproven.append(m[1])
expected = {f"{g}{i}" for g, n in [("K", 12), ("L", 4), ("M", 12), ("N", 13), ("O", 8),
                                    ("P", 8), ("Q", 4), ("R", 4)] for i in range(1, n + 1)}
print(f"entries listed {len(names)} ({len(set(names))} labels; a label on two suites selects both); KILLED labels {len(killed)} of {len(set(names))}; unproven {unproven}; "
      f"not run {sorted(set(names) - set(killed) - set(unproven))}; run twice {[k for k, v in killed.items() if v > 1]}")
print(f"controls (distinct suite/group) {len(controls)}; all PASS {all(all(v == 'PASS' for v in vs) for vs in controls.values())}")
print(f"assertion coverage {len(expected & covered)}/{len(expected)}; missing {sorted(expected - covered)}")
