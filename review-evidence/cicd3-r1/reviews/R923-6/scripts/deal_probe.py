"""Re-deal the hosted Verilator shards with the shipped and a raised gptp_shadow figure.
Usage: python3 -I deal_probe.py <checkout> [gptp_shadow_seconds ...]
Read-only: imports the checkout's scripts/suite_shards.py, edits nothing."""
import sys, importlib.util
from pathlib import Path
root = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("suite_shards", root / "scripts" / "suite_shards.py")
ss = importlib.util.module_from_spec(spec); spec.loader.exec_module(ss)
suites = ss.expand_suites(ss.sweep_suites(root / "tb" / "verilator"))
wf = (root / ".github/workflows/rtl.yml").read_text()
limits = ss.verilator_worker_limits(wf)
total = len(ss.WORKER_OVERHEAD_SECONDS)
print(f"workers={total} budget={ss.CI_BUDGET_SECONDS} headroom={ss.HEADROOM_PERCENT}% limits(min)={sorted(set(limits))}")
for fig in [ss.SUITE_SECONDS["gptp_shadow"]] + [int(a) for a in sys.argv[2:]]:
    sec = dict(ss.SUITE_SECONDS); sec["gptp_shadow"] = fig
    owners, load = ss.balance(suites, total, sec)
    shipped_owners, _ = ss.balance(suites, total, ss.SUITE_SECONDS)
    # stale-deal projection: keep the shipped deal, add the delta to gptp_shadow's worker
    stale = list(_)
    w = shipped_owners["gptp_shadow"]; stale[w] += fig - ss.SUITE_SECONDS["gptp_shadow"]
    print(f"\n gptp_shadow={fig}: shipped deal worker {w} -> {stale[w]} s; max over workers {max(stale)} s")
    over_stale = [(i, l) for i, l in enumerate(stale) if l > ss.CI_BUDGET_SECONDS and i < total - len(ss.DEDICATED_SUITES)]
    print("  shipped-deal regular workers over budget:", over_stale)
    over = [(i, l, l - ss.CI_BUDGET_SECONDS) for i, l in enumerate(load) if l > ss.CI_BUDGET_SECONDS]
    print("  re-dealt loads over budget (idx,load,over):", over)
    print("  re-dealt max:", max(load), " dedicated:", [load[i] for i in range(total - len(ss.DEDICATED_SUITES), total)])
    print("  headroom vs job limits (stale deal):", [(i, l, limits[i]*60*ss.HEADROOM_PERCENT//100) for i, l in enumerate(stale) if l > limits[i]*60*ss.HEADROOM_PERCENT//100])
    print("  hard limit vs stale deal:", [(i, l, limits[i]*60) for i, l in enumerate(stale) if l >= limits[i]*60])
