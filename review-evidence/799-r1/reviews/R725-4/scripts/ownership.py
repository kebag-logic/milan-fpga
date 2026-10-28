"""Usage: python3 -I ownership.py <clone> <receipts-dir>
Checks that the 19 `run_all_suites.sh --ci-pieces --shard i/19 --list` outputs
own every CI unit exactly once, against the planner's own expanded inventory,
and that pinned and dedicated owners hold."""
import sys
from collections import Counter
from pathlib import Path
clone, receipts = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(clone / "scripts"))
import suite_shards as s  # noqa: E402
owners = {}
counts = Counter()
for i in range(19):
    for unit in (receipts / f"list-{i}.log").read_text().split():
        counts[unit] += 1
        owners[unit] = i
inventory = s.expand_suites(s.sweep_suites(clone / "tb" / "verilator"))
print("units listed:", sum(counts.values()), "distinct:", len(counts), "inventory:", len(inventory))
print("duplicates:", sorted(u for u, c in counts.items() if c != 1))
print("missing:", sorted(set(inventory) - set(counts)), "extra:", sorted(set(counts) - set(inventory)))
print("pins:", {u: owners.get(u) for u in s.PINNED_SUITES}, "dedicated:", {u: owners.get(u) for u in s.DEDICATED_SUITES})
print("worker 18 units:", sorted(u for u, w in owners.items() if w == 18))
_, load = s.balance(inventory, 19)
print("predicted per worker:", load)
limits = s.verilator_worker_limits((clone / ".github/workflows/rtl.yml").read_text())
print("workflow limits (min):", limits)
print("60% bound per worker:", [m * 60 * s.HEADROOM_PERCENT // 100 for m in limits])
ok = (all(c == 1 for c in counts.values()) and set(counts) == set(inventory) and len(inventory) == 81
      and all(owners.get(u) == w for u, w in s.PINNED_SUITES.items())
      and owners.get("milan_dp_mclk__0") == 18 and len(limits) == 19)
print("OWNERSHIP", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
