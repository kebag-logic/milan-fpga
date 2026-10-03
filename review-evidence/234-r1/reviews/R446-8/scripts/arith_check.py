#!/usr/bin/env python3
"""R446-8: recompute the derived figures that round 7 wrote into
docs/design/AREA_BUDGET.md and docs/findings/234_PP_SHADOW_AREA_BASELINE.md
from the committed record (syn/ooc/pp_resource_baseline.json at the head), the
first record (at d5f56313) and PR #634's published hierarchy (C side).
usage: arith_check.py <repo> <head>"""
import json
import subprocess
import sys

repo, head = sys.argv[1:3]


def rec(rev):
    out = subprocess.run(["git", "-C", repo, "show", f"{rev}:syn/ooc/pp_resource_baseline.json"],
                         check=True, capture_output=True, text=True).stdout
    return json.loads(out)["endpoints"]


C, A = rec(head), rec("d5f56313dc5a5c2716211356f99796664dc843dd")
cr, ar = C["route-1x1"]["record"], A["route-1x1"]["record"]
cf, af = cr["figures"], ar["figures"]
bad = 0


def eq(label, got, doc):
    global bad
    ok = got == doc
    bad += not ok
    print(f"{'OK  ' if ok else 'FAIL'} {label}: computed {got!r}, document {doc!r}")


eq("LUT % of 63,400", f"{100 * cf['LUT'] / 63400:.2f}", "80.07")
eq("LUT over 38,040", cf["LUT"] - 38040, 12727)
eq("FF % of 126,800", f"{100 * cf['FF'] / 126800:.2f}", "47.03")
eq("slice % of 15,850", f"{100 * cf['SLICE'] / 15850:.2f}", "99.89")
eq("slices free", 15850 - cf["SLICE"], 18)
eq("BRAM tile %", f"{100 * cf['BRAM_TILE'] / 135:.2f}", "68.52")
eq("RAMB36 % of 135", f"{100 * cf['RAMB36'] / 135:.2f}", "58.52")
eq("RAMB18 % of 270", f"{100 * cf['RAMB18'] / 270:.2f}", "10.00")
eq("DSP % of 240", f"{100 * cf['DSP'] / 240:.2f}", "5.83")
eq("C minus A LUT", cf["LUT"] - af["LUT"], 639)
eq("C minus A FF", cf["FF"] - af["FF"], 628)
eq("C minus A SLICE", cf["SLICE"] - af["SLICE"], 17)
eq("C minus A CARRY4", cf["CARRY4"] - af["CARRY4"], 101)
eq("C minus A WNS", round(cf["WNS_ns"] - af["WNS_ns"], 3), 0.13)
eq("C minus A WHS", round(cf["WHS_ns"] - af["WHS_ns"], 3), -0.012)
eq("LUT over tolerance vs first record", cf["LUT"] - af["LUT"] - 500, 139)
eq("FF over tolerance vs first record", cf["FF"] - af["FF"] - 600, 28)
eq("WNS fall to floor", round(cf["WNS_ns"] - 0.03, 3), 0.163)
eq("fall to floor < 0.25 (floor binds first)", cf["WNS_ns"] - 0.03 < 0.25, True)
w = cr["scopes"]["wrapper"]
eq("routed wrapper LUT", w["LUT"], 23904)
eq("routed wrapper LUT change", w["LUT"] - ar["scopes"]["wrapper"]["LUT"], -33)
eq("routed wrapper FF change", w["FF"] - ar["scopes"]["wrapper"]["FF"], 2)
eq("wrapper ceiling for NFR-RES-01", w["LUT"] - (cf["LUT"] - 38040), 11177)
eq("cut share of wrapper %", round(100 * (cf["LUT"] - 38040) / w["LUT"]), 53)
s1 = C["ooc-1x1"]["record"]["figures"]
eq("standalone 1x1 % of device", f"{100 * s1['LUT'] / 63400:.1f}", "38.4")
# C side from PR #634's published hierarchical report (receipts/cross_checks.log section 4)
mdp_c, mdp_ff_c, meter, meter_ff, cpu_c, soc_c = 42200, 48433, 483, 630, 3524, 4847
mdp_a, mdp_ff_a, cpu_a, soc_a = 41527, 47804, 3526, 4857  # first record's history section
eq("milan_datapath % of device", f"{100 * mdp_c / 63400:.1f}", "66.6")
eq("rest of milan_datapath, C", mdp_c - meter - w["LUT"], 17813)
eq("rest of milan_datapath, A", mdp_a - ar["scopes"]["wrapper"]["LUT"], 17590)
eq("rest of milan_datapath FF, C", mdp_ff_c - meter_ff - w["FF"], 23538)
eq("rest of milan_datapath FF, A", mdp_ff_a - ar["scopes"]["wrapper"]["FF"], 23541)
eq("remaining top-level LUT change", (cf["LUT"] - af["LUT"]) - (mdp_c - mdp_a) - (cpu_c - cpu_a) - (soc_c - soc_a), -22)
eq("meter share of LUT growth %", round(100 * meter / (cf["LUT"] - af["LUT"])), 76)
eq("levers 1-5 leave C near", round((cf["LUT"] - 3600) / 100) * 100, 47200)
eq("... percent of device", round(100 * (cf["LUT"] - 3600) / 63400), 74)
eq("... above NFR-RES-01", round((cf["LUT"] - 3600 - 38040) / 100) * 100, 9100)
for ep, d1, d2 in (("ooc-1x1", -11, 1), ("ooc-8x8", -6, 8)):
    c, a = C[ep]["record"]["figures"], A[ep]["record"]["figures"]
    eq(f"{ep} LUT change", c["LUT"] - a["LUT"], d1)
    eq(f"{ep} FF change", c["FF"] - a["FF"], d2)
    for k in ("RAMB36", "RAMB18", "DSP", "CARRY4", "BRAM_TILE", "WNS_ns"):
        eq(f"{ep} {k} unchanged", c[k] - a[k], 0)
print(f"mismatches: {bad}")
sys.exit(1 if bad else 0)
