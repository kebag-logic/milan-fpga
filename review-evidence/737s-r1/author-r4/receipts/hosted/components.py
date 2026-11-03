"""Round 4 (#737): every elaborate component's largest value over the frozen cited-run set, from the jobs API."""
import json
import sys
from datetime import datetime

CITED = [
    "41470524727-a1", "41476923392-a1", "41476923392-a2", "41476923392-a3",
    "41526004847-a1", "41554508699-a1", "41583428850-a1",
    "41678609075-a1", "41678609075-a2", "41678609075-a3",  # jobs-a1/a2/a3.json of round 3
    "41705989293-a1", "41705989293-a2",
]
FILES = {"41678609075-a1": "jobs-a1.json", "41678609075-a2": "jobs-a2.json", "41678609075-a3": "jobs-a3.json"}
# member verdict rows, LiteX legs on workers of their own (leg receipts / job logs)
ROWS = {
    "41583428850-a1": dict(cpu=70, ctrl=280, gmii=0, gptp=461, boot=25, mem=14, retained=331, soc=240),
    "41678609075-a1": dict(cpu=72, ctrl=224, gmii=0, gptp=246, boot=25, mem=15, retained=336, soc=369),
    "41678609075-a3": dict(cpu=71, ctrl=284, gmii=0, gptp=462, boot=25, mem=14, retained=333, soc=510),
    "41705989293-a1": dict(cpu=52, ctrl=240, gmii=0, gptp=459, boot=18, mem=11, retained=236, soc=409),
    "41705989293-a2": dict(cpu=70, ctrl=277, gmii=0, gptp=477, boot=25, mem=14, retained=331, soc=472),
}
LEGS = [["gptp"], ["cpu", "gmii", "boot", "mem", "retained"], ["ctrl", "soc"]]
# run 41583428850 ran the legs it was later re-derived from (job logs: leg 0 soc; leg 1 gmii, gptp, boot, mem; leg 2 cpu, ctrl, retained)
LEGS_BY_RUN = {"41583428850-a1": [["soc"], ["gmii", "gptp", "boot", "mem"], ["cpu", "ctrl", "retained"]]}
DEPTH_ONE = {"Cancel late CI failures", "Fail fast across this head"}


def t(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").timestamp()


def span(x):
    return int(t(x["completed_at"]) - t(x["started_at"]))


best = {}


def keep(name, value, where):
    if value > best.get(name, (-1, ""))[0]:
        best[name] = (value, where)


for run in CITED:
    jobs = json.load(open(FILES.get(run, f"jobs-{run}.json")))["jobs"]
    print(f"== {run}")
    for j in jobs:
        if not j.get("started_at") or not j.get("completed_at"):
            continue
        steps = j["steps"]
        sp = span(j)
        co = next((span(s) for s in steps if s["name"] == "Run actions/checkout@v4" and s.get("completed_at")), 0)
        name = j["name"]
        if name.startswith("elaborate-gates-"):
            gates = sum(span(s) for s in steps if s["name"].startswith(("Elaboration gates", "Standalone LiteX")) and s.get("completed_at"))
            ver = sum(span(s) for s in steps if s["name"] == "Build Verilator from source on cache miss" and s.get("completed_at"))
            setup = sp - gates - ver
            parts = [f"{s['name']} {span(s)}" for s in steps if s["name"].startswith(("Elaboration gates", "Standalone LiteX")) and s.get("completed_at")]
            print(f"  {name:28} span {sp:5} {j['conclusion']:9} setup {setup:4} verilator {ver:4} checkout {co:4} | {'; '.join(parts)}")
            keep("setup", setup, f"{name} {run}")
            keep("verilator", ver, f"{name} {run}")
            keep(f"span {name}", sp, run)
            for s in steps:
                if s["name"].startswith("Elaboration gates, leg ") and s.get("completed_at"):
                    keep(s["name"][len("Elaboration gates, "):], span(s), run)
                if s["name"].startswith("Standalone LiteX simulation aggregate, leg ") and run in ROWS:
                    leg = int(s["name"].split("leg ")[1].split(" of")[0])
                    rows = sum(ROWS[run][m] for m in LEGS_BY_RUN.get(run, LEGS)[leg])
                    keep("selftest", span(s) - rows, f"{name} {run} ({span(s)} - {rows})")
        else:
            print(f"  {name:28} span {sp:5} {j['conclusion']:9} checkout {co:4} less-checkout {sp - co:4}")
            if name == "elaborate":
                keep("aggregate rest", sp - co, run)
            if name == "Collect CI manifest":
                keep("collector", sp, run)
            if name == "Cancel late CI failures":
                keep("tail", sp, run)
            if name in DEPTH_ONE or (name == "elaborate" and run.startswith("41705989293")):
                keep("depth-one checkout", co, f"{name} {run}")

largest = {m: max(r[m] for r in ROWS.values()) for m in ROWS["41583428850-a1"]}
print("\ncomponent maxima:")
for k in sorted(best):
    print(f"  {k:34} {best[k][0]:5}  {best[k][1]}")
print("LARGEST", largest)
JOB, HEADROOM = 2700, 600
SETUP, VER, SELF = best["setup"][0], best["verilator"][0], best["selftest"][0]
LEG0, LEG1 = best["leg 0 of 2"][0], best["leg 1 of 2"][0]
budget = JOB - HEADROOM - SETUP - VER - SELF
held = [sum(largest[m] for m in leg) for leg in LEGS]
print(f"LEG_BUDGET = {JOB} - {HEADROOM} - {SETUP} - {VER} - {SELF} = {budget}; legs at LARGEST {held}; fit {all(h <= budget for h in held)}")
proj = {"elaborate-gates-0": SETUP + LEG0, "elaborate-gates-1": SETUP + LEG1}
for i, h in enumerate(held):
    proj[f"elaborate-gates-{i + 2} (cold)"] = SETUP + VER + SELF + h
for k, v in proj.items():
    print(f"  {k:28} {v:5} against {JOB}, margin {JOB - v}, to the {JOB - HEADROOM} line {JOB - HEADROOM - v}")
warm_litex = [SETUP + SELF + h for h in held]
print("  LiteX with Verilator restored", warm_litex)
agg = best["depth-one checkout"][0] + best["aggregate rest"][0]
allowance = agg + best["collector"][0] + 120 + best["tail"][0]
print(f"aggregate {best['depth-one checkout'][0]} + {best['aggregate rest'][0]} = {agg}, margin under 180: {180 - agg}")
print(f"allowance {agg} + {best['collector'][0]} + 120 + {best['tail'][0]} = {allowance}")
warm = max(proj["elaborate-gates-0"], proj["elaborate-gates-1"], *warm_litex)
cold = max(proj.values())
print(f"workflow warm {warm} + {allowance} = {warm + allowance} ({(warm + allowance) / 60:.1f} min, {warm + allowance - 1800} over 1800)")
print(f"workflow cold {cold} + {allowance} = {cold + allowance} ({(cold + allowance) / 60:.1f} min, {cold + allowance - 1800} over 1800)")
print(f"with the aggregate kept at 104: allowance {104 + best['collector'][0] + 120 + best['tail'][0]}")
sys.exit(0 if all(h <= budget for h in held) and max(proj.values()) <= JOB - HEADROOM else 1)
