#!/usr/bin/env python3
"""Cross-check the #696 re-baseline figures written in AREA_BUDGET.md and the
#234 findings page against syn/ooc/pp_resource_baseline.json at a given rev."""
import json, subprocess, sys
repo, rev, prev_rev = sys.argv[1], sys.argv[2], sys.argv[3]
show = lambda p: subprocess.run(["git", "-C", repo, "show", f"{rev}:{p}"], check=True,
                                capture_output=True, text=True).stdout
base = json.loads(show("syn/ooc/pp_resource_baseline.json"))["endpoints"]
budget = show("docs/design/AREA_BUDGET.md"); find = show("docs/findings/234_PP_SHADOW_AREA_BASELINE.md")
sec = find.split("## Re-baseline of 2026-10-10, issue #696", 1)[1].split("\n## ", 1)[0]
fails = 0
def need(text, s, why):
    global fails
    ok = s in text; fails += not ok
    print(("ok  " if ok else "FAIL"), why, repr(s))
g = lambda n: base[n]["record"]["figures"]
r, o1, o8 = g("route-1x1"), g("ooc-1x1"), g("ooc-8x8")
c = lambda v: f"{v:,}"
need(sec, f"| `route-1x1` | {c(r['LUT'])} | {c(r['FF'])} | {c(r['SLICE'])} | {r['RAMB36']} / {r['RAMB18']} | {r['DSP']} | {c(r['CARRY4'])} | +{r['WNS_ns']:.3f} | +{r['WHS_ns']:.3f} |", "findings route row")
for n, f in (("ooc-1x1", o1), ("ooc-8x8", o8)):
    need(sec, f"| `{n}` | {c(f['LUT'])} | {c(f['FF'])} | - | {f['RAMB36']} / {f['RAMB18']} | {f['DSP']} | {c(f['CARRY4'])} | {f['WNS_ns']:.3f} | +{f['WHS_ns']:.3f} |", f"findings {n} row")
for n in base:
    need(sec, f"| `{n}` | `{base[n]['record']['inputs_sha256']}` |", f"findings {n} input sha")
pct = lambda a, b: f"{100*a/b:.2f} %"
need(budget, f"| Slice LUT | 63,400 | {c(r['LUT'])} | {pct(r['LUT'],63400)} |", "budget LUT row")
need(budget, f"not met, {c(r['LUT']-38040)} over", "budget LUT over")
need(budget, f"| Slice register | 126,800 | {c(r['FF'])} | {pct(r['FF'],126800)} |", "budget FF row")
need(budget, f"| Slice | 15,850 | {c(r['SLICE'])} | {pct(r['SLICE'],15850)} | must stay below the device to place | {15850-r['SLICE']} free |", "budget slice row")
need(budget, f"| Block RAM tile | 135 | {r['BRAM_TILE']} |", "budget BRAM row")
need(budget, f"| DSP | 240 | {r['DSP']} |", "budget DSP row")
need(budget, f"+{r['WNS_ns']:.3f} / +{r['WHS_ns']:.3f} ns", "budget WNS/WHS")
need(budget, f"placement has {15850-r['SLICE']} slices left", "budget slices left")
w = base["route-1x1"]["record"]["scopes"]["wrapper"]["LUT"]
need(budget, f"The wrapper names {c(w)} of them", "budget wrapper LUT")
need(sec, f"of which the wrapper uses {c(w)}", "findings wrapper LUT")
need(budget, f"needs the wrapper at most {c(38040-(r['LUT']-w))} LUTs", "budget wrapper ceiling")
need(budget, f"removing {c(r['LUT']-38040)} LUTs, {round(100*(r['LUT']-38040)/w)} % of the wrapper", "budget removal")
fl = base["route-1x1"]["floor"]["WNS_ns"]; tol = base["route-1x1"]["tolerance"]["WNS_ns"]
need(budget, f"At the current +{r['WNS_ns']:.3f} ns WNS record, the absolute +{fl:.3f} ns floor binds first, after a fall of {r['WNS_ns']-fl:.3f} ns", "budget binding limit")
print("binding check: floor", fl, ">", r['WNS_ns'] - tol, "=", fl > r['WNS_ns'] - tol)
fails += not (fl > r['WNS_ns'] - tol)
prev = json.loads(subprocess.run(["git", "-C", repo, "show", f"{prev_rev}:syn/ooc/pp_resource_baseline.json"],
                                 capture_output=True, text=True, check=True).stdout)["endpoints"]
p = prev["route-1x1"]["record"]["figures"]
d = lambda k: r[k] - p[k]
need(sec, f"| `route-1x1` | {d('LUT'):+d} | {d('FF'):+d} | {d('SLICE'):+d} | {d('WNS_ns'):+.3f} | {d('WHS_ns'):+.3f} |", "findings delta row")
need(budget, f"its route moved by {d('LUT'):+d} LUTs, {d('FF'):+d} FFs and {d('SLICE'):+d} slices, with WNS {d('WNS_ns'):+.3f} ns and WHS {d('WHS_ns'):+.3f} ns", "budget seventh delta")
need(budget, f"The preceding [#645](https://github.com/kebag-logic/milan-fpga/issues/645) image used {c(p['LUT'])} LUTs and {c(p['SLICE'])} slices, {15850-p['SLICE']} free, at +{p['WNS_ns']:.3f} / +{p['WHS_ns']:.3f} ns", "budget preceding image")
for n in ("ooc-1x1", "ooc-8x8"):
    pf, nf = prev[n]["record"]["figures"], base[n]["record"]["figures"]
    same = pf == nf; fails += not same; print("ok  " if same else "FAIL", n, "figures equal to preceding record")
print("FAILURES", fails); sys.exit(1 if fails else 0)
