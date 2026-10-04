#!/usr/bin/env python3
"""R466 probe: from a reviewer-reproduced sweep work directory (pp-ship, pp-si3,
pp-si5, pp-si9; and adp-if-1/2/4), refit the processor stream-context model and the
ADP marginals with the committed resmap_models code, and print the per-step
increments that decide whether the growth is faster or slower than linear.
Usage: pp_stream_fit.py <repo> <work dir>"""
import json, sys
from pathlib import Path
repo, work = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(repo / "syn/resmap"))
import resmap_models as RM, yosys_sweep as YS
plan = YS.load_plan(YS.PLAN)
summary = json.loads((work / "summary.json").read_text())
models = RM.parameter_models(plan, summary)
key = "N_SPORT_IN_P+N_SPORT_OUT_P+N_STREAM_IN_P+N_STREAM_OUT_P"
m = models[key]
print("points", [(r["point"], r["x"], r["LUT"]) for r in m["data"]])
print("LUT fit", m["LUT"]["coefficients"], "rms", m["LUT"]["rms"], "max", m["LUT"]["max_abs"], "residuals", m["LUT"]["residuals"])
print("FF fit", m["FF"]["coefficients"], "rms", m["FF"]["rms"])
d = m["data"]
for a, b in zip(d, d[1:]):
    print(f"step x {a['x']:.0f}->{b['x']:.0f}: +{b['LUT']-a['LUT']:.0f} LUT total, {(b['LUT']-a['LUT'])/(b['x']-a['x']):.0f} per stream")
marg = RM.marginals(plan, summary, "KL_pp_shadow", "pp-ship")
for n in ("pp-si3", "pp-si5", "pp-si9"):
    print(n, "delta", marg[n]["delta"], "top moved", [(b, c["LUT"]) for b, c in marg[n]["moved"][:3]])
adp = RM.marginals(plan, summary, "KL_adp_engine", "adp-if-1")
for n, e in adp.items():
    print(n, "delta", e["delta"])
