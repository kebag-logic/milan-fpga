#!/usr/bin/env python3
"""Plant faults into scratch copies of recorded #814 route sets and require the head gate's verdicts.

usage: route_probes.py <gate.py> <scratch dir> <dev set root> <control set root> <out dir>
Each probe copies a set's three directories (reports only, no checkpoints), rebinds the comparison scripts to the
copy's shipping checkpoint path, applies its plant, runs the gate, and checks exit status and required/forbidden text.
"""
import json, re, shutil, subprocess, sys
from pathlib import Path

GATE, SCRATCH, DEV, CTRL, OUT = map(Path, sys.argv[1:6])
SKIP = shutil.ignore_patterns("*.dcp", ".Xil", "*.cache", "*.hw", "*.ip_user_files", "*.xpr", "*.v", "*.init")
SUBS = ("ax7101/gateware", "ax7101-AltSpreadLogic_high", "ax7101-ExtraTimingOpt")
OUT.mkdir(parents=True, exist_ok=True)

def copy(src: Path, name: str) -> Path:
    root = SCRATCH / name
    if root.exists():
        shutil.rmtree(root)
    for sub in SUBS:
        shutil.copytree(src / sub, root / sub, ignore=SKIP, symlinks=True)
    for sub in SUBS[1:]:
        tcl = root / sub / "baseline_implementation.tcl"
        tcl.write_text(tcl.read_text().replace(str(src / SUBS[0]), str(root / SUBS[0])))
    return root

def summary(path: Path, column: int, value: str) -> None:
    """Rewrite one column (0 WNS, 4 WHS) of the Design Timing Summary value row of a report."""
    text = path.read_text()
    head, mark, body = text.partition("| Design Timing Summary")
    lines = body.split("\n")
    nonblank = [i for i, line in enumerate(lines) if line.strip()]
    heads = next(k for k, i in enumerate(nonblank) if "WNS(ns)" in lines[i])
    row = nonblank[heads + 2]
    parts = re.split(r"(\s+)", lines[row])
    values = [k for k, p in enumerate(parts) if p and not p.isspace()]
    k = values[column]
    old = parts[k]
    parts[k] = value.rjust(len(old))
    if len(parts[k]) > len(old) and k > 0 and len(parts[k - 1]) > len(parts[k]) - len(old):
        parts[k - 1] = parts[k - 1][: len(parts[k - 1]) - (len(parts[k]) - len(old))]
    lines[row] = "".join(parts)
    path.write_text(head + mark + "\n".join(lines))

def corner(root: Path, sub: str, name: str) -> Path:
    return root / sub / f"alinx_ax7101_signoff_{name}_timing.rpt"

def gate(*args: str) -> tuple[int, str]:
    r = subprocess.run([sys.executable, "-B", str(GATE), *args], capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout + r.stderr

def setargs(root: Path, cmd: str = "check", extra: tuple = ()) -> list[str]:
    return [cmd, str(root / SUBS[0]), "--endpoint", "route-1x1", "--comparison", str(root / SUBS[1]),
            "--comparison", str(root / SUBS[2]), *extra]

results = []
def probe(name: str, args: list[str], rc: int, need: tuple = (), forbid: tuple = ()) -> None:
    got, text = gate(*args)
    ok = got == rc and all(n in text for n in need) and not any(f in text for f in forbid)
    (OUT / f"{name}.log").write_text(f"$ gate {' '.join(args)}\n{text}\nrc={got}\n")
    results.append({"probe": name, "want_rc": rc, "rc": got, "need": need, "forbid": forbid, "ok": ok})
    print(f"{'PASS' if ok else 'FAIL'} {name}: rc={got} want {rc}")

S, A, E = SUBS
# Controls on unmodified copies.
r = copy(DEV, "dev-control"); probe("dev-control", setargs(r), 0, ("directive ExtraPostPlacementOpt selected", "RESULT: PASS"))
r = copy(CTRL, "ctrl-control"); probe("ctrl-control", setargs(r), 0, ("directive AltSpreadLogic_high selected", "RESULT: PASS"))

# (1) The selected (best-WNS) route misses the hold floor at ONE corner only.
r = copy(DEV, "best-whs-one-corner")
summary(corner(r, S, "Fast_85C"), 4, "-0.004"); summary(r / S / "baseline_timing.rpt", 4, "-0.004")
probe("best-whs-one-corner", setargs(r), 1, ("directive ExtraPostPlacementOpt selected",
      "REGRESSION: below the floor 0.0 at Fast_85C"), ("at Fast_0C, Fast_85C", "RESULT: PASS"))
# (1b) The best route misses the setup floor at one corner, every route below it so it stays the best.
r = copy(DEV, "best-wns-one-corner")
summary(corner(r, S, "Slow_85C"), 0, "0.020"); summary(r / S / "baseline_timing.rpt", 0, "0.020")
for sub, v in ((A, "0.015"), (E, "0.010")):
    for c in ("Slow_0C", "Slow_85C"):
        summary(corner(r, sub, c), 0, v)
    summary(r / sub / "baseline_timing.rpt", 0, v)
probe("best-wns-one-corner", setargs(r), 1, ("directive ExtraPostPlacementOpt selected",
      "REGRESSION: below the floor 0.03 at Slow_85C"), ("Slow_0C, Slow_85C", "RESULT: PASS"))
# (1c) A non-selected comparison below the floor at every corner does not fail the set.
r = copy(DEV, "other-below-floor")
for c in ("Slow_0C", "Slow_85C"):
    summary(corner(r, E, c), 0, "-0.200")
summary(r / E / "baseline_timing.rpt", 0, "-0.200")
probe("other-below-floor", setargs(r), 0, ("directive ExtraPostPlacementOpt selected", "RESULT: PASS"))
# Issue case 2: the shipping directive misses the floor, the best meets it: pass naming the best.
r = copy(DEV, "shipping-misses-best-meets")
for c in ("Slow_0C", "Slow_85C"):
    summary(corner(r, S, c), 0, "0.010")
summary(r / S / "baseline_timing.rpt", 0, "0.010")
probe("shipping-misses-best-meets", setargs(r), 0, ("directive AltSpreadLogic_high selected", "RESULT: PASS"),
      ("REGRESSION",))
# The same shipping route judged alone, marked: fails on the floor.
probe("shipping-misses-marked-alone", ["check", str(r / S), "--endpoint", "route-1x1", "--shipping-selection"], 1,
      ("below the floor 0.03 at Slow_0C, Slow_85C",))
# (3) A large fall passes with a WARNING (selected WNS 0.040 against the 0.44 record), never a failure.
r = copy(DEV, "large-fall")
for sub, v in ((S, "0.040"), (A, "0.035"), (E, "0.031")):
    for c in ("Slow_0C", "Slow_85C"):
        summary(corner(r, sub, c), 0, v)
    summary(r / sub / "baseline_timing.rpt", 0, v)
probe("large-fall", setargs(r), 0, ("WARNING: fell by more than 0.25 from the record", "RESULT: PASS"), ("REGRESSION",))
# Issue case 4 and (3): a resource over tolerance on the selected route still fails; on a non-selected one it does not.
def lut(path: Path, delta: int) -> None:
    text = path.read_text()
    m = re.search(r"(\| Slice LUTs\*?\s*\|\s*)(\d+)", text)
    path.write_text(text[:m.start(2)] + str(int(m[2]) + delta).rjust(len(m[2])) + text[m.end(2):])
r = copy(CTRL, "selected-lut-over")
lut(r / A / "baseline_utilization.rpt", 700)
probe("selected-lut-over", setargs(r), 1, ("directive AltSpreadLogic_high selected", "REGRESSION: grew by more than"))
r = copy(CTRL, "unselected-lut-over")
lut(r / S / "baseline_utilization.rpt", 700)
probe("unselected-lut-over", setargs(r), 0, ("directive AltSpreadLogic_high selected", "RESULT: PASS"))
# (2) Gaming: a comparison script that is not the snippet's (one extra command).
r = copy(DEV, "comparison-extra-command")
t = r / A / "baseline_implementation.tcl"; t.write_text(t.read_text().replace("place_design -directive", "set_param place.timingDriven 1\nplace_design -directive", 1))
probe("comparison-extra-command", setargs(r), 2, ("is not the script the recipe writes",))
# A comparison opening another route's synthesis checkpoint (different inputs).
r = copy(DEV, "comparison-other-checkpoint")
t = r / A / "baseline_implementation.tcl"; t.write_text(t.read_text().replace(str(r / S), str(CTRL / S), 1))
probe("comparison-other-checkpoint", setargs(r), 2, ("does not open the shipping checkpoint",))
# A comparison of another thread setting.
r = copy(DEV, "comparison-threads")
t = r / E / "baseline_implementation.tcl"; t.write_text(t.read_text().replace("maxThreads 32", "maxThreads 8", 1))
probe("comparison-threads", setargs(r), 2, ("not the shipping route's",))
# A comparison at the shipping directive (two ExtraPostPlacementOpt) and two comparisons at one directive.
r = copy(DEV, "comparison-shipping-directive")
t = r / A / "baseline_implementation.tcl"; t.write_text(t.read_text().replace("-directive AltSpreadLogic_high", "-directive ExtraPostPlacementOpt"))
probe("comparison-shipping-directive", setargs(r), 2, ("is not the script the recipe writes",))
r = copy(DEV, "duplicate-comparison")
probe("duplicate-comparison", ["check", str(r / S), "--endpoint", "route-1x1", "--comparison", str(r / A),
      "--comparison", str(r / A)], 2, ("holds each of",))
probe("one-comparison", ["check", str(r / S), "--endpoint", "route-1x1", "--comparison", str(r / A)], 2, ("holds each of",))
probe("shipping-as-comparison", ["check", str(r / S), "--endpoint", "route-1x1", "--comparison", str(r / S),
      "--comparison", str(r / E)], 2, ("NOT COMPARABLE",))
probe("set-and-mark", setargs(r, extra=("--shipping-selection",)), 2, ("or alone with --shipping-selection",))
# A comparison of another tool build (identity): edit the Tool Version header of every report it reads.
r = copy(DEV, "comparison-tool")
for f in (r / E).glob("*.rpt"):
    f.write_text(f.read_text().replace("Build 6511674", "Build 6511675", 1))
probe("comparison-tool", setargs(r), 2, ("tool or recipe change in tool",))
# A comparison of another population: remove a control engine's cells from its census.
r = copy(DEV, "comparison-population")
cells = r / E / "baseline_hierarchy.rpt"
cells.write_text("".join(l for l in cells.read_text().splitlines(True) if "KL_adp_engine" not in l))
probe("comparison-population", setargs(r), 2, ("ExtraTimingOpt: ", "wrong placement"))
# An incomplete comparison route, not selected, fails the set naming its directive.
r = copy(DEV, "comparison-unrouted")
st = r / E / "alinx_ax7101_route_status.rpt"
txt = st.read_text(); m = re.search(r"(# of nets with routing errors\.*\s*:\s*)(\d+)", txt)
st.write_text(txt[:m.start(2)] + "3".rjust(len(m[2])) + txt[m.end(2):])
probe("comparison-unrouted", setargs(r), 1, ("ROUTE INCOMPLETE: ExtraTimingOpt:",))
# A missing corner report on a comparison, and a corner from another run (worst disagrees with the summary).
r = copy(DEV, "comparison-corner-missing")
corner(r, A, "Fast_85C").unlink()
probe("comparison-corner-missing", setargs(r), 2, ("alinx_ax7101_signoff_Fast_85C_timing.rpt",))
r = copy(DEV, "selected-corner-foreign")
shutil.copy2(corner(CTRL, S, "Slow_85C"), corner(r, S, "Slow_85C"))
probe("selected-corner-foreign", setargs(r), 2, ("the reports are not of one run",))
# (3) Record: --write of a set into a scratch baseline stores the selected route, names its directive, and re-checks.
r = copy(CTRL, "record-write")
repo = GATE.parents[2]
base = SCRATCH / "record-write" / "baseline.json"; shutil.copy2(repo / "syn/ooc/pp_resource_baseline.json", base)
probe("record-write", setargs(r, "record", ("--baseline", str(base), "--write")), 0, ("directive AltSpreadLogic_high selected",))
rec = json.loads(base.read_text())["endpoints"]["route-1x1"]["record"]
ok = "place_design -directive AltSpreadLogic_high" in rec["identity"]["flow"] and rec["figures"]["WNS_ns"] == 0.342
results.append({"probe": "record-write-content", "ok": ok, "WNS_ns": rec["figures"]["WNS_ns"]})
print(f"{'PASS' if ok else 'FAIL'} record-write-content: WNS {rec['figures']['WNS_ns']}")
probe("record-write-recheck", setargs(r, extra=("--baseline", str(base))), 0, ("directive AltSpreadLogic_high selected", "RESULT: PASS"))
probe("record-write-marked-shipping", ["check", str(r / S), "--endpoint", "route-1x1", "--shipping-selection",
      "--baseline", str(base)], 0, ("RESULT: PASS",))
probe("record-write-baseline", ["check-baseline", "--baseline", str(base)], 0, ("baseline PASS",))
(OUT / "results.json").write_text(json.dumps(results, indent=1) + "\n")
bad = [x["probe"] for x in results if not x["ok"]]
print(f"route probes: {len(results) - len(bad)} PASS, {len(bad)} FAIL {bad}")
sys.exit(1 if bad else 0)
