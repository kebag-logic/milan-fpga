"""Runner-minutes before and after, from the 20 measured successful runs of each workflow (means).

A divided job's legs run the same main work, so after = the job's mean window plus (legs - 1) times its mean
time outside its main step (checkout, installs, caches, evidence), plus each added job's own estimate."""
import json, datetime, statistics, collections
from pathlib import Path
H = Path(__file__).resolve().parents[1] / "hosted"
t = lambda s: datetime.datetime.fromisoformat(s)
win, main = collections.defaultdict(list), collections.defaultdict(list)
per_run = collections.defaultdict(lambda: collections.defaultdict(float))
runs = {w: [r["id"] for r in json.loads((H / f"{w}-runs.json").read_text())["workflow_runs"]]
        for w in ("rtl-fast", "rtl-full", "elaborate", "docs")}
MAIN = {"firmware-control-mutants": "Run the control mutation campaign", "firmware-aecp-mutants": "Run the AECP mutation campaign",
        "firmware-srp-mutants": "Run both SRP mutation campaigns and pin controls",
        "publication-census": "Run the publication census in every shape the builder builds"}
UNIT = ("Prove the tally", "Run the control-plane", "Run the saved-state", "Hold the firmware coverage")
for w, ids in runs.items():
    for rid in ids:
        for j in json.loads((H / f"{rid}-jobs.json").read_text())["jobs"]:
            if j["conclusion"] == "skipped" or not j.get("completed_at"):
                continue
            d = (t(j["completed_at"]) - t(j["started_at"])).total_seconds()
            per_run[w][rid] += d
            if j["conclusion"] != "success":
                continue
            win[(w, j["name"])].append(d)
            steps = {s["name"]: (t(s["completed_at"]) - t(s["started_at"])).total_seconds()
                     for s in j["steps"] if s.get("started_at") and s.get("completed_at") and s["conclusion"] != "skipped"}
            if j["name"] in MAIN:
                main[j["name"]].append(steps.get(MAIN[j["name"]], 0) + (steps.get("Build Yosys from source on cache miss", 0)
                                                                     if j["name"] == "publication-census" else 0))
            elif j["name"] == "firmware-unit":
                main[j["name"]].append(sum(v for k, v in steps.items() if k.startswith(UNIT)))
            elif w == "docs" and j["name"] == "docs-gates-1":
                main[j["name"]].append(sum(v for k, v in steps.items() if k.startswith("End-station builder gates")))
m = lambda k: statistics.mean(win[k])
outside = {n: statistics.mean(win[("rtl-fast", n)]) - statistics.mean(main[n]) for n in (*MAIN, "firmware-unit")}
print("mean outside the main step, s:", {k: round(v) for k, v in outside.items()})
before = {w: statistics.mean(per_run[w].values()) / 60 for w in runs}
print("mean runner-minutes per run, before (all hosted jobs, watchers included):", {k: round(v, 1) for k, v in before.items()})
legs = {"firmware-control-mutants": 4, "firmware-aecp-mutants": 2, "firmware-srp-mutants": 2, "firmware-unit": 3}
added = sum((n - 1) * outside[j] for j, n in legs.items())
# Census: five legs each pay the census job's outside time; the judge runs a checkout, a fetch, a pip install and a
# download (docs-gates-1's checkout-and-install share is the nearest measured figure, taken whole: 60 s). A Yosys
# rebuild no longer happens in the census: its mean share over the 20 runs is subtracted (the tool job builds it).
builds = []
for rid in runs["rtl-fast"]:
    for j in json.loads((H / f"{rid}-jobs.json").read_text())["jobs"]:
        if j["name"] == "publication-census" and j["conclusion"] == "success":
            builds.append(sum((t(s["completed_at"]) - t(s["started_at"])).total_seconds() for s in j["steps"]
                              if s["name"] == "Build Yosys from source on cache miss" and s["conclusion"] == "success"))
saved = statistics.mean(builds)
print("census Yosys builds per run, mean s:", round(saved), "over", len(builds), "runs,", sum(b > 0 for b in builds), "with a build")
added += 4 * outside["publication-census"] + 60 - saved
docs_setup = statistics.mean(win[("docs", "docs-gates-1")]) - statistics.mean(main["docs-gates-1"])
added_docs = 2 * docs_setup
print("added rtl-fast seconds per run:", round(added), "added docs seconds per run:", round(added_docs))
print("after, runner-minutes per run: rtl-fast", round(before["rtl-fast"] + added / 60, 1), "docs", round(before["docs"] + added_docs / 60, 1))
