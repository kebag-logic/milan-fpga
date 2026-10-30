#!/usr/bin/env python3
"""Round-2 probes of the #818 route gate on scratch copies of recorded route sets.

usage: r2_probes.py <gate.py> <scratch dir> <dev set root> <control set root> <out dir>
Reuses route_probes.py's copy/summary helpers (same directory). Each probe checks exit status and required and
forbidden text. F1: the Mark II mapping record command as documented. F2: a floor miss with a fall beyond the
timing fall prints both the REGRESSION and the WARNING and exits 1. F3: a timing summary that disagrees with the
per-corner reports, in both directions, for both slacks, is refused (2). S1: the BRAM tile ceiling on the
selected route only.
"""
import json, re, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
src = (HERE / "route_probes.py").read_text().split("results = []")[0]
ns: dict = {"__name__": "route_probes_helpers"}
sys_argv, sys.argv = sys.argv, sys.argv[:6]
exec(compile(src, "route_probes.py", "exec"), ns)
sys.argv = sys_argv
GATE, SCRATCH, DEV, CTRL, OUT = ns["GATE"], ns["SCRATCH"], ns["DEV"], ns["CTRL"], ns["OUT"]
copy, summary, corner, gate, setargs, SUBS = (ns[k] for k in ("copy", "summary", "corner", "gate", "setargs", "SUBS"))
S, A, E = SUBS
results = []


def probe(name, args, rc, need=(), forbid=(), env=None):
    got, text = gate(*args)
    ok = got == rc and all(n in text for n in need) and not any(f in text for f in forbid)
    (OUT / f"{name}.log").write_text(f"$ gate {' '.join(args)}\n{text}\nrc={got}\n")
    results.append({"probe": name, "want_rc": rc, "rc": got, "need": need, "forbid": forbid, "ok": ok})
    print(f"{'PASS' if ok else 'FAIL'} {name}: rc={got} want {rc}")


def slack_all(root, sub, column, value, corners):
    for c in corners:
        summary(corner(root, sub, c), column, value)
    summary(root / sub / "baseline_timing.rpt", column, value)


SLOW, FAST = ("Slow_0C", "Slow_85C"), ("Fast_0C", "Fast_85C")

# F2 (WNS): every route below the WNS floor at the slow corners and fallen by > 0.25 ns from the 0.44 record.
r = copy(DEV, "f2-wns-floor-and-fall")
slack_all(r, S, 0, "0.020", SLOW); slack_all(r, A, 0, "0.015", SLOW); slack_all(r, E, 0, "0.010", SLOW)
probe("f2-wns-floor-and-fall", setargs(r), 1,
      ("directive ExtraPostPlacementOpt selected",
       "REGRESSION: below the floor 0.03 at Slow_0C, Slow_85C; WARNING: fell by more than 0.25 from the record",
       "WARNING: WNS_ns fell from the record by more than the timing fall", "RESULT: MATERIAL REGRESSION"),
      ("RESULT: PASS",))
# F2, one corner only (the round-1 reproduction): the floor names Slow_85C alone and the WARNING still prints.
r = copy(DEV, "f2-wns-one-corner")
summary(corner(r, S, "Slow_85C"), 0, "0.020"); summary(r / S / "baseline_timing.rpt", 0, "0.020")
slack_all(r, A, 0, "0.015", SLOW); slack_all(r, E, 0, "0.010", SLOW)
probe("f2-wns-one-corner", setargs(r), 1,
      ("REGRESSION: below the floor 0.03 at Slow_85C; WARNING: fell by more than 0.25",
       "WARNING: WNS_ns fell from the record"), ("Slow_0C, Slow_85C", "RESULT: PASS"))
# F2 (WHS): the selected route's hold at -0.300 at the fast corners (record 0.036, fall 0.336 > 0.25).
r = copy(DEV, "f2-whs-floor-and-fall")
slack_all(r, S, 4, "-0.300", FAST)
probe("f2-whs-floor-and-fall", setargs(r), 1,
      ("directive ExtraPostPlacementOpt selected",
       "REGRESSION: below the floor 0.0 at Fast_0C, Fast_85C; WARNING: fell by more than 0.25 from the record",
       "WARNING: WHS_ns fell from the record", "RESULT: MATERIAL REGRESSION"), ("RESULT: PASS",))
# F2 negative: hold below the floor within the timing fall (-0.010; fall 0.046): REGRESSION, no WARNING.
r = copy(DEV, "f2-whs-floor-no-fall")
slack_all(r, S, 4, "-0.010", FAST)
probe("f2-whs-floor-no-fall", setargs(r), 1, ("REGRESSION: below the floor 0.0 at Fast_0C, Fast_85C",
      "RESULT: MATERIAL REGRESSION"), ("WARNING",))
# F2 on the marked single route: the same two notes, exit 1.
probe("f2-whs-marked-alone", ["check", str(r / S), "--endpoint", "route-1x1", "--shipping-selection"], 1,
      ("REGRESSION: below the floor 0.0 at Fast_0C, Fast_85C",), ("WARNING",))
r = copy(DEV, "f2-wns-marked-alone")
slack_all(r, S, 0, "0.010", SLOW)
probe("f2-wns-marked-alone", ["check", str(r / S), "--endpoint", "route-1x1", "--shipping-selection"], 1,
      ("REGRESSION: below the floor 0.03 at Slow_0C, Slow_85C; WARNING: fell by more than 0.25",
       "WARNING: WNS_ns fell from the record", "RESULT: MATERIAL REGRESSION"))

# F3: the summary below every corner report, under the floor (corners unchanged) -> refused, for WNS and WHS.
r = copy(DEV, "f3-summary-wns-below-corners")
for sub in SUBS:
    summary(r / sub / "baseline_timing.rpt", 0, "0.010")
probe("f3-summary-wns-below-corners", setargs(r), 2, ("the reports are not of one run", "worst WNS_ns"),
      ("RESULT: PASS",))
r = copy(DEV, "f3-summary-whs-below-corners")
summary(r / S / "baseline_timing.rpt", 4, "-0.050")
probe("f3-summary-whs-below-corners", setargs(r), 2, ("the reports are not of one run", "worst WHS_ns"),
      ("RESULT: PASS",))
probe("f3-summary-whs-below-corners-marked", ["check", str(r / S), "--endpoint", "route-1x1", "--shipping-selection"],
      2, ("the reports are not of one run", "timing summary's -0.05"))
# F3 the other direction: one corner below the summary (summary unchanged) -> refused, for WNS and WHS.
r = copy(DEV, "f3-corner-wns-below-summary")
summary(corner(r, S, "Slow_0C"), 0, "0.100")
probe("f3-corner-wns-below-summary", setargs(r), 2, ("the reports are not of one run", "worst WNS_ns is 0.1"))
r = copy(DEV, "f3-corner-whs-below-summary")
summary(corner(r, A, "Fast_0C"), 4, "0.001")
probe("f3-corner-whs-below-summary", setargs(r), 2, ("the reports are not of one run", "worst WHS_ns is 0.001"))


# S1: the BRAM tile ceiling (121.5) is judged on the selected route only.
def bram(path: Path, value: str) -> None:
    text = path.read_text()
    m = re.search(r"(\| Block RAM Tile\s*\|\s*)([\d.]+)", text)
    path.write_text(text[:m.start(2)] + value.rjust(len(m[2])) + text[m.end(2):])


r = copy(CTRL, "s1-selected-over-ceiling")
bram(r / A / "baseline_utilization.rpt", "130")
probe("s1-selected-over-ceiling", setargs(r), 1, ("directive AltSpreadLogic_high selected",
      "BRAM_TILE  REGRESSION: 130 exceeds the ceiling 121.5"))
r = copy(CTRL, "s1-unselected-over-ceiling")
bram(r / S / "baseline_utilization.rpt", "130")
probe("s1-unselected-over-ceiling", setargs(r), 0, ("directive AltSpreadLogic_high selected", "RESULT: PASS"),
      ("exceeds the ceiling",))

# F1: the MARK_II_AREA_PLAN.md mapping record, verbatim from the doc but for $WORK, then a check against it.
repo = Path(GATE).parents[2]
work = copy(DEV, "f1-mark2")
doc = (repo / "docs/design/MARK_II_AREA_PLAN.md").read_text()
block = doc[doc.index("A Mark II lane maps its own route the same way."):]
block = block[block.index("```sh\n") + 6:]
block = block[:block.index("\n```")]
joined = block.replace("\\\n", " ").split("\n")
cp_line = next(l for l in joined if l.startswith("cp "))
rec_line = next(l for l in joined if l.startswith("python3 syn/ooc/pp_resource_gate.py record"))
(OUT / "f1-documented-lines.txt").write_text(cp_line + "\n" + rec_line + "\n")
script = f"set -e\ncd {repo}\nWORK={work}\n{cp_line}\n{rec_line}\n"
p = subprocess.run(["bash", "-c", script], capture_output=True, text=True, env={"PATH": "/usr/bin:/bin",
                   "PYTHONDONTWRITEBYTECODE": "1"})
(OUT / "f1-mark2-record.log").write_text(script + "---\n" + p.stdout + p.stderr + f"\nrc={p.returncode}\n")
rec = json.loads((work / "scratch_baseline.json").read_text())["endpoints"]["route-1x1"]["record"] \
    if (work / "scratch_baseline.json").exists() else {}
ok = p.returncode == 0 and "place_design -directive ExtraPostPlacementOpt" in rec.get("identity", {}).get("flow", "") \
    and rec.get("figures", {}).get("WNS_ns") == 0.303
results.append({"probe": "f1-mark2-record", "rc": p.returncode, "ok": ok, "WNS_ns": rec.get("figures", {}).get("WNS_ns")})
print(f"{'PASS' if ok else 'FAIL'} f1-mark2-record: rc={p.returncode} WNS {rec.get('figures', {}).get('WNS_ns')}")
probe("f1-mark2-recheck", ["check", str(work / S), "--endpoint", "route-1x1", "--shipping-selection",
      "--baseline", str(work / "scratch_baseline.json")], 0, ("RESULT: PASS",))
probe("f1-mark2-unmarked-refused", ["record", str(work / S), "--endpoint", "route-1x1",
      "--baseline", str(work / "scratch_baseline.json")], 2, ("NOT COMPARABLE",))

(OUT / "results.json").write_text(json.dumps(results, indent=1) + "\n")
bad = [x["probe"] for x in results if not x["ok"]]
print(f"round-2 probes: {len(results) - len(bad)} PASS, {len(bad)} FAIL {bad}")
sys.exit(1 if bad else 0)
