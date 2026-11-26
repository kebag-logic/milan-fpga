"""Project each divided job's slowest leg on the hosted runner, and its 1.41x figure.

A leg's share of its campaign is its local verdict-time share (the legs ran side by side on one host); the
projection gives that share of the slowest hosted window of the undivided step over the 20 measured runs, plus
the job's slowest time outside that step. Census legs: their local wall times, the same way."""
import datetime, json, re, statistics
from pathlib import Path
R = Path(__file__).resolve().parents[1]
H, L = R / "hosted", R / "local"
t = lambda s: datetime.datetime.fromisoformat(s)
def windows(job, step_prefixes):
    out = []
    for f in H.glob("*-jobs.json"):
        for j in json.loads(f.read_text())["jobs"]:
            if j["name"] != job or j["conclusion"] != "success":
                continue
            steps = {s["name"]: (t(s["completed_at"]) - t(s["started_at"])).total_seconds()
                     for s in j["steps"] if s.get("started_at") and s.get("completed_at") and s["conclusion"] != "skipped"}
            main = sum(v for k, v in steps.items() if k.startswith(step_prefixes))
            out.append(((t(j["completed_at"]) - t(j["started_at"])).total_seconds(), main))
    return out
def leg_seconds(path):
    lines = path.read_text().splitlines()
    return float(lines[-1].split()[0]) - float(lines[0].split()[0])
rows = []
def campaign(job, prefix, legs):
    w = windows(job, (prefix,))
    step, outside = max(m for _, m in w), max(a - m for a, m in w)
    secs = [leg_seconds(p) for p in legs]
    share = max(secs) / sum(secs)
    proj = step * share + outside
    rows.append((job, max(a for a, _ in w), len(legs), round(share * 100, 1), round(proj), round(proj * 1.41)))
campaign("firmware-control-mutants", "Run the control mutation campaign", sorted((L / "control").glob("leg?.log")))
campaign("firmware-aecp-mutants", "Run the AECP mutation campaign", sorted((L / "aecp-srp").glob("aecp-leg?.log")))
campaign("firmware-srp-mutants", "Run both SRP mutation campaigns", sorted((L / "aecp-srp").glob("srp-leg?.log")))
w = windows("publication-census", ("Run the publication census",))
step, outside = max(m for _, m in w), max(a - m for a, m in w if True)
outside = max(a - m - b for (a, m), b in zip(w, [0] * len(w)))
secs = [leg_seconds(p) for p in sorted((L / "census").glob("leg?.log"))]
share = max(secs) / sum(secs)
census_out = sorted(a - m for a, m in w)
# A census window outside its step held a Yosys build in 6 runs; the legs restore the tool tree instead, so the
# outside figure is the largest of the runs without a build.
no_build = [a - m for a, m in w if a - m < 300]
proj = step * share + max(no_build)
rows.append(("publication-census-legs", max(a for a, _ in w), 5, round(share * 100, 1), round(proj), round(proj * 1.41)))
u = {}
for prefix, leg in (("Prove the tally", 0), ("Run the control-plane", 0), ("Run the saved-state", 1), ("Hold the firmware coverage", 2)):
    u.setdefault(leg, []).append(prefix)
wu = windows("firmware-unit", tuple(p for v in u.values() for p in v))
outside_u = max(a - m for a, m in wu)
for leg, prefixes in u.items():
    m = max(mm for _, mm in windows("firmware-unit", tuple(prefixes)))
    rows.append((f"firmware-unit leg {leg}", max(a for a, _ in wu), 3, "-", round(m + outside_u), round((m + outside_u) * 1.41)))
print(f"{'job':28s} {'slowest before':>14s} {'legs':>4s} {'max share %':>11s} {'slowest leg':>11s} {'x1.41':>6s}")
for r in rows:
    print(f"{r[0]:28s} {r[1]:14.0f} {r[2]:4d} {str(r[3]):>11s} {r[4]:11d} {r[5]:6d}")
