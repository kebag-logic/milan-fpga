#!/usr/bin/env python3
"""Plant regressions and refusals through pp_resource_gate.py's own command line.

Usage: probe_cli.py <repo checkout> <scratch dir> [gate.py to drive instead of the checkout's]
Builds a synthetic recipe measurement directory with the shipped self-test's
fixture builder, records it into a baseline that carries the REAL route-1x1 /
ooc-1x1 policy from syn/ooc/pp_resource_baseline.json, then runs the CLI as a
subprocess per planted change and compares the exit status with the documented
one (0 within tolerance, 1 material regression, 2 not comparable/unreadable).
Writes nothing inside the checkout. Prints one line per probe and a tally.
"""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys

repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
ooc = repo / "syn/ooc"
gate_py = Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else ooc / "pp_resource_gate.py"
sys.path.insert(0, str(gate_py.parent))
import pp_resource_gate as gate  # noqa: E402
import pp_resource_gate_selftest as st  # noqa: E402

real = json.loads((ooc / "pp_resource_baseline.json").read_text())["endpoints"]
shutil.rmtree(scratch, ignore_errors=True)
scratch.mkdir(parents=True)
results = []


def cli(*args):
    run = subprocess.run([sys.executable, "-B", str(gate_py), *map(str, args)], capture_output=True, text=True)
    return run.returncode, (run.stdout + run.stderr).strip()


def setup(kind):
    root = scratch / kind
    root.mkdir()
    folder = st.fixture(root / "arm", kind)
    entry = copy.deepcopy({k: v for k, v in real["route-1x1" if kind == "route" else "ooc-1x1"].items()
                           if k != "record"})
    entry["record"] = gate.record(folder, kind)
    (root / "arm").rename(root / "pristine")
    baseline = root / "baseline.json"
    baseline.write_text(json.dumps({"endpoints": {"ep": entry}}))
    return root, baseline, entry


def probe(kind, root, baseline, label, plants, want, needle="", endpoint="ep", base_override=None):
    folder = st.fresh(root, kind)
    for name, old, new in plants:
        st.plant(folder, name.replace("{repo}", str(root / "arm/repo")), old, new)
    path = baseline
    if base_override is not None:
        path = root / "override.json"
        path.write_text(base_override)
    status, out = cli("check", folder, "--endpoint", endpoint, "--baseline", path)
    ok = status == want and needle in out
    results.append(ok)
    last = [line for line in out.splitlines() if line.strip()][-1] if out else ""
    print(f"{'OK  ' if ok else 'BAD '} {kind:<5} {label}: exit {status}, documented {want} | {last[:150]}")


SRC = st.SOURCE
row = st.row
T = st.TIMING
# The fixture's figures: LUT 1000, FF 2000 (repeated row), SLICE 400, BRAM_TILE 4.5, RAMB36 4, RAMB18 1, DSP 2,
# WNS 0.500, WHS 0.100.
ff = lambda new: (row("FF", 2000, new), ("baseline_utilization.rpt", st.REPEATED, st.REPEATED.replace("2000", str(new))))
root, base, entry = setup("route")
pol = entry
print("route policy under test:", json.dumps({k: pol[k] for k in ("tolerance", "floor", "ceiling")}))
P = lambda *a, **k: probe("route", root, base, *a, **k)
P("control, changed source only", (SRC,), 0, "RESULT: PASS")
P("LUT +500 (at tolerance)", (SRC, row("LUT", 1000, 1500)), 0, "RESULT: PASS")
P("LUT +501", (SRC, row("LUT", 1000, 1501)), 1, "LUT")
P("FF +600 (at tolerance)", (SRC, *ff(2600)), 0, "RESULT: PASS")
P("FF +601", (SRC, *ff(2601)), 1, "FF")
P("SLICE +80 (at tolerance)", (SRC, row("SLICE", 400, 480)), 0, "RESULT: PASS")
P("SLICE +81", (SRC, row("SLICE", 400, 481)), 1, "SLICE")
P("RAMB36 +1", (SRC, row("RAMB36", 4, 5)), 1, "RAMB36")
P("RAMB18 +1", (SRC, row("RAMB18", 1, 2)), 1, "RAMB18")
P("DSP +1", (SRC, row("DSP", 2, 3)), 1, "DSP")
P("BRAM tiles 121.5 (at ceiling)", (SRC, row("BRAM_TILE", 4.5, 121.5)), 0, "RESULT: PASS")
P("BRAM tiles 122 (over ceiling)", (SRC, row("BRAM_TILE", 4.5, 122)), 1, "ceiling")
P("WNS +0.300 (fall 0.200, above floor)", (SRC, (T, "  0.500  ", "  0.300  ")), 0, "RESULT: PASS")
P("WNS +0.250 (fall exactly 0.25)", (SRC, (T, "  0.500  ", "  0.250  ")), 0, "RESULT: PASS")
P("WNS +0.249 (fall 0.251)", (SRC, (T, "  0.500  ", "  0.249  ")), 1, "fell by")
P("WHS 0.000 (at floor)", (SRC, (T, "0.100", "0.000")), 0, "RESULT: PASS")
P("WHS -0.001 (below floor)", (SRC, (T, "0.100", "-0.001")), 1, "below the floor")
P("tool build changed", (("baseline_utilization.rpt", "Build 6511674", "Build 6511675"),), 2, "tool")
P("device changed", (("baseline_utilization.rpt", "xc7a100tfgg484-2", "xc7a200tfbg484-2"),), 2, "device")
P("route directive changed", (("baseline_integrated.tcl", "AggressiveExplore", "Explore"),), 2, "flow")
P("thread count changed", (("baseline_integrated.tcl", "maxThreads 32", "maxThreads 8"),), 2, "flow")
P("design state changed", (("baseline_utilization.rpt", "Physopt postRoute", "Routed"),), 2, "state")
P("identical inputs, LUT differs", (row("LUT", 1000, 1001),), 2, "identical inputs")
P("utilization report missing", (("baseline_utilization.rpt", None, None),), 2, "NOT COMPARABLE")
P("hierarchy report missing", (("baseline_hierarchy.rpt", None, None),), 2, "NOT COMPARABLE")
P("cell census missing", (("baseline_cells.tsv", None, None),), 2, "NOT COMPARABLE")
P("images manifest missing", (("baseline_images.json", None, None),), 2, "NOT COMPARABLE")
P("images manifest malformed JSON", (("baseline_images.json", None, "{not json"),), 2, "NOT COMPARABLE")
P("images manifest wrong shape", (("baseline_images.json", None, '["a"]'),), 2, "NOT COMPARABLE")
P("utilization row malformed", (row("DSP", 2, "two"),), 2, "not a count")
P("timing summary missing", ((T, "| Design Timing Summary", "| Design Timing"),), 2, "NOT COMPARABLE")
P("timing value row truncated", ((T, "      0.500        0.000                      0                   10        0.100        0.000\n", ""),), 2, "NOT COMPARABLE")
P("duplicate Tool Version header", (("baseline_utilization.rpt", "| Design       :", "| Tool Version : Vivado v.2025.2 (lin64) Build 1\n| Design       :"),), 2, "Tool Version")
P("unknown endpoint", (), 2, "", endpoint="nope")
good = json.loads(base.read_text())
bad = copy.deepcopy(good); del bad["endpoints"]["ep"]["record"]
P("baseline endpoint without record", (SRC,), 2, "", base_override=json.dumps(bad))
P("baseline file malformed JSON", (SRC,), 2, "", base_override="{")
bad = copy.deepcopy(good); del bad["endpoints"]["ep"]["tolerance"]["LUT"]
P("baseline tolerance missing (check)", (SRC,), 2, "", base_override=json.dumps(bad))
bad = copy.deepcopy(good); bad["endpoints"]["ep"]["ceiling"] = {"BRAM_TILES": 121.5}
P("baseline ceiling names no figure (check)", (SRC,), 2, "", base_override=json.dumps(bad))

root, base, entry = setup("ooc")
print("ooc policy under test:", json.dumps({k: entry[k] for k in ("tolerance",)}))
O = lambda *a, **k: probe("ooc", root, base, *a, **k)
O("control, changed source only", (SRC,), 0, "RESULT: PASS")
O("LUT +250 (at tolerance)", (SRC, row("LUT", 1000, 1250)), 0, "RESULT: PASS")
O("LUT +251", (SRC, row("LUT", 1000, 1251)), 1, "LUT")
O("FF +251", (SRC, *ff(2251)), 1, "FF")
O("RAMB36 +1", (SRC, row("RAMB36", 4, 5)), 1, "RAMB36")
O("RAMB18 +1", (SRC, row("RAMB18", 1, 2)), 1, "RAMB18")
O("DSP +1", (SRC, row("DSP", 2, 3)), 1, "DSP")
O("standalone clock 20 -> 10 ns", (("clock.xdc", "20.000", "10.000"),), 2, "standalone_clock_ns")
O("standalone clock file missing", (("clock.xdc", None, None),), 2, "")
O("route script beside ooc script", (("baseline_integrated.tcl", None, "quit\n"),), 2, "recipe scripts")

# Baseline-level checks through the CLI: a policy edit check-baseline does or does not refuse.
real_path = ooc / "pp_resource_baseline.json"
for label, edit, want in (
        ("real baseline", lambda b: None, 0),
        ("route WNS floor removed", lambda b: b["endpoints"]["route-1x1"]["floor"].pop("WNS_ns"), 2),
        ("route LUT tolerance negative", lambda b: b["endpoints"]["route-1x1"]["tolerance"].__setitem__("LUT", -1), 2),
        ("route ceiling removed (policy weakened)", lambda b: b["endpoints"]["route-1x1"].pop("ceiling"), "observe"),
        ("route LUT tolerance 10**9 (policy weakened)",
         lambda b: b["endpoints"]["route-1x1"]["tolerance"].__setitem__("LUT", 10**9), "observe"),
        ("ooc-1x1 record removed", lambda b: b["endpoints"]["ooc-1x1"].pop("record"), 2)):
    data = json.loads(real_path.read_text())
    edit(data)
    path = scratch / "edited_baseline.json"
    path.write_text(json.dumps(data))
    status, out = cli("check-baseline", "--baseline", path)
    ok = want == "observe" or status == want
    results.append(ok)
    last = out.splitlines()[-1] if out else ""
    print(f"{'OK  ' if ok else 'BAD '} base  {label}: check-baseline exit {status}, expected {want} | {last[:150]}")

print(f"probes: {sum(results)} as documented, {len(results) - sum(results)} not, of {len(results)}")
