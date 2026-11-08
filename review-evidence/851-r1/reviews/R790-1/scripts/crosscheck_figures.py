#!/usr/bin/env python3
"""Cross-check the route and gate figures in the PR #852 evidence against the
committed baseline JSON. Usage: crosscheck_figures.py EVIDENCE_851_R1_DIR REPO_DIR
[DEV_ROUTE_GATE_LOG]. Prints one line per figure; exit 1 on a mismatch."""
import json, re, sys, pathlib
ev, repo = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
dev_log = pathlib.Path(sys.argv[3]) if len(sys.argv) > 3 else None
bad = 0
def chk(name, got, exp):
    global bad
    ok = got == exp
    bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {name}: receipt={got} expected={exp}")
head = json.loads((ev / "author/receipts/route-2d939d2d/head-2d939d2d.json").read_text())
chk("shipping route LUT", head["lut"]["used"], 53033.0)
chk("shipping route FF", head["ff"]["used"], 54729.0)
chk("shipping route slices", head["slice"]["used"], 15792.0)
chk("shipping route WNS worst", head["wns_worst"], 0.044)
chk("shipping route WHS worst", head["whs_worst"], 0.035)
chk("shipping route routing errors", head["routing_errors"], 0)
for c, v in head["corners"].items():
    chk(f"corner {c} WNS>=0.030", v["wns"] >= 0.030, True)
    chk(f"corner {c} WHS>=0", v["whs"] >= 0.0, True)
gate = (ev / "author/receipts/gate/gate-route-1x1.log").read_text()
def fig(text, name):
    m = re.search(rf"^{name}\s+(\S+)\s+(\S+)\s+(\S+)", text, re.M)
    return [float(x) for x in m.groups()]
base = json.loads((repo / "syn/ooc/pp_resource_baseline.json").read_text())
rec = base["endpoints"]["route-1x1"]["record"]["figures"]
for f in ("LUT", "FF", "SLICE", "WNS_ns", "WHS_ns"):
    chk(f"gate route candidate {f} == committed record", fig(gate, f)[1], float(rec[f]))
for ep, logname in (("ooc-1x1", "gate-ooc-1x1.log"), ("ooc-8x8", "gate-ooc-8x8.log")):
    t = (ev / "author/receipts/gate" / logname).read_text()
    r = base["endpoints"][ep]["record"]["figures"]
    for f in ("LUT", "FF"):
        chk(f"{ep} candidate {f} == committed record", fig(t, f)[1], float(r[f]))
for m in re.finditer(r"^\s+(Slow|Fast)_\w+\s+WNS_ns\s+(\S+)\s+WHS_ns\s+(\S+)", gate, re.M):
    chk(f"selected route corner {m.group(0).split()[0]} meets floors",
        float(m.group(2)) >= 0.030 and float(m.group(3)) >= 0.0, True)
if dev_log:
    d = dev_log.read_text()
    dl, ds, dw = fig(d, "LUT")[1], fig(d, "SLICE")[1], fig(d, "WNS_ns")[1]
    print(f"INFO dev 1eb5289d selected route: LUT {dl:.0f} SLICE {ds:.0f} WNS {dw}")
    print(f"INFO adoption share on the selected route: LUT {rec['LUT']-dl:+.0f} SLICE {rec['SLICE']-ds:+.0f} WNS {rec['WNS_ns']-dw:+.3f}")
wsp = (ev / "author/receipts/route-2d939d2d/worst-setup-path.txt").read_text()
m = re.search(r"Slack \(MET\) :\s+(\S+)ns", wsp)
print(f"INFO worst-setup-path.txt slack {m.group(1)} ns; route WNS {head['wns_worst']} ns; "
      f"{'CONSISTENT' if abs(float(m.group(1))-head['wns_worst'])<1e-9 else 'NOT THE WORST PATH'}")
sys.exit(1 if bad else 0)
