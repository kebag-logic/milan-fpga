#!/usr/bin/env python3
"""The Arty's correction pair from math: read a row (zero, sum) computed from a tap capture at a known applied pair, derive the pair, write it, read it back; caller holds the bench lock.
usage: setpair.py <row.json> true|tap <transcript> [egress_ns] [target_pdelay_ns]
true: egress is the assignment (default 100 ns, DP83848 note 4 and T2.6.1) and ingress the rest of the sum, so the Arty's difference lands on the zero.
tap:  the row's applied pair, which must be the true pair, plus extra egress only, 2 x (zero - target), so PDELAY_NS lands on the target (default 650 ns); refuses a prediction not under 800 ns."""
import json, subprocess, sys
row = json.load(open(sys.argv[1])); mode = sys.argv[2]; out = sys.argv[3]
egr = int(sys.argv[4]) if len(sys.argv) > 4 else 100
target = float(sys.argv[5]) if len(sys.argv) > 5 else 650.0
S, zero = row["sum"], row["zero"]
if mode == "tap":
    # the applied pair of the row is the true pair; extra egress only
    ing, egr = row["ingress"], row["egress"]
    extra = round(2 * (zero - target))
    assert extra >= 0
    egr += extra
    pred = zero + (S - ing - egr) / 2
    assert 0 < pred < 800, pred
else:
    ing = round(S - egr)
    pred = zero + (S - ing - egr) / 2
print(f"from {row['dir']}: zero {zero} sum {S} -> ingress {ing} egress {egr}, predicted PDELAY_NS {pred:.1f}")
sys.exit(subprocess.run(["python3", "$VALIDATION_STORAGE/829-a725b/tools/lat.py", out, "write", str(ing), str(egr)]).returncode)
