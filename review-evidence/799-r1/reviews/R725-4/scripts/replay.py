"""Usage: python3 -I replay.py <clone> <union-measure-output>
Charges the head's own 19-worker balance with the largest hosted window of each
unit in the given --measure output (table figure where a unit has no window),
plus the head's 122 s allowance, against each worker's workflow limit."""
import re
import sys
from pathlib import Path
clone = Path(sys.argv[1])
sys.path.insert(0, str(clone / "scripts"))
import suite_shards as s  # noqa: E402
text = Path(sys.argv[2]).read_text().split("== union", 1)[1]
measured = {k: int(v) for k, v in re.findall(r'"([a-z0-9_]+)": (\d+),', text)}
inventory = s.expand_suites(s.sweep_suites(clone / "tb" / "verilator"))
owners, load = s.balance(inventory, 19)
limits = s.verilator_worker_limits((clone / ".github/workflows/rtl.yml").read_text())
regular = sum(s.SUITE_SECONDS[u] for u in inventory if u not in s.DEDICATED_SUITES)
print("regular work (table):", regular, "16-worker capacity:", 16 * (1620 - 122))
print("unwindowed (table figure charged):", sorted(u for u in inventory if u not in measured))
changed_up = sorted(f"{u} {s.SUITE_SECONDS[u]}<{measured[u]}" for u in inventory if u in measured and measured[u] > s.SUITE_SECONDS[u])
print("table below measured:", changed_up)
print("worker predicted measured limit_s")
over = 0
for w in range(19):
    units = [u for u in inventory if owners[u] == w]
    m = s.WORKER_OVERHEAD_SECONDS[w] + sum(measured.get(u, s.SUITE_SECONDS[u]) for u in units)
    lim = limits[w] * 60
    over += m >= lim
    print(f"{w:2d}/19 {load[w]:5d} {m:5d} {lim:5d} {'OVER' if m >= lim else 'under'}{' >1620' if m > 1620 and w < 18 else ''} {','.join(units)}")
print("placements:", {u: owners[u] for u in ("media_phase", "follow_ring", "gptp_tables", "mmcm_servo")})
print("workers at or over limit:", over)
sys.exit(1 if over else 0)
