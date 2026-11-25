#!/usr/bin/env python3
"""Compare the CI policy's Verilator projection table with the planner's own balance at a checkout."""
import re, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "scripts"))
import suite_shards as s  # noqa: E402
suites = s.expand_suites(s.sweep_suites(root / "tb/verilator"))
total = len(s.WORKER_OVERHEAD_SECONDS)
owners, load = s.balance(suites, total)
doc = (root / "docs/testing/CI_WORKFLOWS.md").read_text()
rows = {int(m[1]): (int(m[3]), int(m[4]), int(m[5])) for m in re.finditer(r"\| `verilator-shards (\d+)/(\d+)` \| (\d+) \| (\d+) \| (\d+) \|", doc)}
bad = 0
print(f"units={len(suites)} workers={total} table_rows={len(rows)}")
for w in range(total):
    want = load[w]
    got = rows.get(w)
    ok = got is not None and got[0] == want and got[1] - got[0] == got[2]
    bad += not ok
    print(f"worker {w}: planner {want} table {got} {'ok' if ok else 'MISMATCH'}")
extra = sorted(set(rows) - set(range(total)))
bad += len(extra)
for name in ("input_loopback", "input_loopback_dp"):
    print(name, "-> worker", owners.get(name))
print("RESULT", "PASS" if bad == 0 else f"FAIL ({bad})")
sys.exit(1 if bad else 0)
