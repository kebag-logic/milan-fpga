"""Independent recompute of the elaborate components from run 41705989293 attempts 1 and 2 (jobs API)."""
import json, sys
from datetime import datetime
ROWS = {  # verdict rows read from the hosted job logs, by leg
    1: [[459], [52, 0, 18, 11, 236], [240, 409]],
    2: [[477], [70, 0, 25, 14, 331], [277, 472]],
}
def t(s): return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").timestamp()
def sp(x): return int(t(x["completed_at"]) - t(x["started_at"]))
base = sys.argv[1]
for a in (1, 2):
    jobs = json.load(open(f"{base}/jobs-41705989293-a{a}.json"))["jobs"]
    print(f"== attempt {a}")
    for j in sorted(jobs, key=lambda j: j["name"]):
        s = sp(j)
        steps = {st["name"]: sp(st) for st in j["steps"] if st.get("completed_at") and st.get("started_at")}
        if j["name"].startswith("elaborate-gates-"):
            w = int(j["name"].rsplit("-", 1)[1])
            gate = {k: v for k, v in steps.items() if k.startswith(("Elaboration gates", "Standalone LiteX"))}
            ver = steps.get("Build Verilator from source on cache miss", 0)
            setup = s - sum(gate.values()) - ver
            extra = ""
            if w >= 2:
                (gname, gsec), = gate.items()
                rows = sum(ROWS[a][w - 2])
                extra = f" leg-step {gsec} rows {rows} selftest {gsec - rows}"
            co = steps.get("Run actions/checkout@v4", 0)
            inst = steps.get("Install LiteX at the pinned revisions", 0)
            print(f"  {j['name']} {j['conclusion']} span {s} setup {setup} verilator {ver} checkout {co} litex-install {inst} gates {gate}{extra}")
        else:
            co = steps.get("Run actions/checkout@v4", 0)
            print(f"  {j['name']} {j['conclusion']} span {s} checkout {co} rest {s - co}")
