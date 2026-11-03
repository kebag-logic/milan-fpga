"""Per-job spans, gate steps, Verilator builds and setup for the cited elaborate runs (#737 round 2)."""
import json, sys
from datetime import datetime as D
from pathlib import Path

def t(s):
    return D.fromisoformat(s.replace("Z", "+00:00")).timestamp()

BUILD = "Build Verilator from source on cache miss"
for path in sys.argv[1:]:
    jobs = json.loads(Path(path).read_text())["jobs"]
    t0 = min(t(j["started_at"]) for j in jobs if j["started_at"])
    ends = [t(j["completed_at"]) for j in jobs if j["completed_at"]]
    print(f"== {Path(path).stem}: first start..last end {max(ends) - t0:.0f} s")
    for j in sorted(jobs, key=lambda j: j["name"]):
        if not j["started_at"] or not j["completed_at"]:
            print(f"  {j['name']}: incomplete"); continue
        s, e, c = t(j["started_at"]), t(j["completed_at"]), t(j["created_at"])
        steps = {st["name"]: t(st["completed_at"]) - t(st["started_at"]) for st in j["steps"]
                 if st["started_at"] and st["completed_at"]}
        gates = {n: v for n, v in steps.items() if n.startswith(("Elaboration gates", "Standalone LiteX"))}
        build = steps.get(BUILD, 0)
        pre = 0
        for st in j["steps"]:
            if st["name"].startswith("Standalone LiteX"):
                pre = t(st["started_at"]) - s
        line = (f"  {j['name']:26} queued {s - c:5.0f} start+{s - t0:5.0f} end+{e - t0:5.0f} span {e - s:5.0f}"
                f" {j['conclusion']}")
        if j["name"].startswith("elaborate-gates"):
            line += (f" | gates {sum(gates.values()):5.0f} verilator-build {build:4.0f}"
                     f" setup {e - s - sum(gates.values()) - build:4.0f}"
                     + "".join(f" | {n} {v:.0f}" for n, v in gates.items()))
            if pre:
                line += f" | before LiteX step {pre:.0f}, span less LiteX step {e - s - next(v for n, v in gates.items() if n.startswith('Standalone')):.0f}"
        print(line)
