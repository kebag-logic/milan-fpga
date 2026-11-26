"""Per-step hosted durations of the named jobs over the measured runs (median and max)."""
import json, sys, statistics, datetime, collections
from pathlib import Path
H = Path(__file__).resolve().parents[1] / "hosted"
want = set(sys.argv[1:])
d = collections.defaultdict(list)
tot = collections.defaultdict(list)
for f in sorted(H.glob("*-jobs.json")):
    for j in json.loads(f.read_text())["jobs"]:
        if j["name"] not in want or j["conclusion"] != "success":
            continue
        t = lambda s: datetime.datetime.fromisoformat(s)
        tot[j["name"]].append((t(j["completed_at"]) - t(j["started_at"])).total_seconds())
        for s in j["steps"]:
            if s.get("started_at") and s.get("completed_at") and s["conclusion"] != "skipped":
                d[(j["name"], s["number"], s["name"])].append((t(s["completed_at"]) - t(s["started_at"])).total_seconds())
for name in sorted(want):
    v = tot[name]
    print(f"== {name}: n={len(v)} median={statistics.median(v):.0f} max={max(v):.0f}")
    for (n, num, step), v in sorted(d.items()):
        if n == name and max(v) >= 5:
            print(f"   {num:2d} {step[:70]:70s} med {statistics.median(v):6.0f} max {max(v):6.0f} n {len(v)}")
