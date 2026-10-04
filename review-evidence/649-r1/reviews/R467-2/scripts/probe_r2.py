#!/usr/bin/env python3
"""Round-2 mutation probes on a disposable copy of the head tree (never the clone).

Usage: probe_r2.py <copy root containing syn/resmap and syn/ooc> <published inputs/map dir>

Part 1 runs round 1's probe_partition.py arm B verbatim against the head module.
Part 2 disables each tie (and each sub-check) of resmap_map.py in turn and runs
--selftest: a tie whose removal leaves the self-test passing has no arm.
Part 3 does the same for the round-2 guard, rank and page-check code in
resmap_models.py and resmap_tables.py, plus the two remaining round-1 sweep arms.
Part 4 plants wrong figures in a copy of the REAL published map inputs and runs
`resmap_map.py map`: a wrong leaf LUT figure outside the processor scopes, and a
census LUT cell moved to another LUT letter.
Every mutated file is restored byte for byte after its arm.
"""
import importlib.util, shutil, subprocess, sys, tempfile
from pathlib import Path

root = Path(sys.argv[1]); mapdir = Path(sys.argv[2]); d = root / "syn" / "resmap"


def run_mutant(what, name, old, new, expect_fail=True):
    f = d / name; orig = f.read_bytes(); text = orig.decode()
    n = text.count(old)
    if n != 1:
        print(f"{what:70s} -> SITE NOT FOUND ({n})"); return
    f.write_text(text.replace(old, new))
    try:
        r = subprocess.run([sys.executable, "-B", str(f), "--selftest"], capture_output=True, text=True)
    finally:
        f.write_bytes(orig)
    last = (r.stdout.strip().splitlines() or [r.stderr.strip()[-100:]])[-1]
    verdict = "KILLED (self-test fails)" if r.returncode else "SURVIVED (self-test passes)"
    flag = "" if bool(r.returncode) == expect_fail else "   <-- unexpected"
    print(f"{what:70s} -> {verdict}: {last}{flag}")


print("== Part 1: round-1 probe_partition.py arm B, verbatim, against the head module")
spec = importlib.util.spec_from_file_location("rm", d / "resmap_map.py"); m = importlib.util.module_from_spec(spec)
sys.dont_write_bytecode = True; spec.loader.exec_module(m)
with tempfile.TemporaryDirectory() as tmp:
    t = Path(tmp); figures, scopes = m._fixture(t)
    m._plant(t, "map_hierarchy.rpt", "|   leaf | m | 2 | 2 |", "|   leaf | m | 7 | 7 |")
    try:
        res = m.build(t, figures, scopes)
        print("ARM B (leaf LUT 2 -> 7): TIED CLEAN; adjustment at top =", res["adjustments"]["top"]["LUT"])
    except m.TieError as e:
        print("ARM B (leaf LUT 2 -> 7): caught:", str(e).replace("\n", " | "))

print("== Part 2: each tie / sub-check of resmap_map.py disabled, then --selftest")
MAP = [
    ("ancestry: additive columns exact", "if delta[column]:\n", "if False:\n"),
    ("ancestry: LUT sharing adjustment never positive", "if delta[column] > 0:", "if False:"),
    ("census: leaf FF/RAMB/DSP cell counts", "if counted != rows[leaf][column]:", "if False:"),
    ("census: every row's four LUT columns vs distinct LUT sites", "if counted != rows[key][column]:", "if False:"),
    ("census: stray owner (cell owned by a non-leaf row)", "    if stray:\n", "    if False:\n"),
    ("flat report: top row and slices", "if abs(top.get(column, -1) - value) > 1e-6:", "if False:"),
    ("record: totals", "elif abs(top.get(column, -1) - figures[column]) > 1e-6:", "elif False:"),
    ("record: a recorded scope's columns", "if mine.get(column) != value:", "if False:"),
    ("record: a recorded scope missing from the map (append dropped)",
     "            failures.append(f\"record: scope {scope!a} is not in the map\")\n", ""),
    ("depth: truncation", "if depth >= requested_depth(report):", "if False:"),
    ("guard (stated implied): census totals equal the top row", "        if total != rows[root][column]:", "        if False:"),
    ("guard (stated implied): top own cells by name sum to its row",
     "if sum(entry[column] for entry in by_name.values()) != rows[f\"{root}/@own\"][column]:", "if False:"),
]
for what, old, new in MAP:
    run_mutant(what, "resmap_map.py", old, new, expect_fail="implied" not in what)

print("== Part 3: guard fail-closed, rank, page check, sweep arms")
OTHER = [
    ("models: a missing guard record read as clean", "resmap_models.py",
     '        raise GuardError(f"{name}: no guard record; run yosys_sweep.py guards, then summary")',
     "        return []"),
    ("models: a hard-error guard record read as clean", "resmap_models.py",
     "    if guards.get(\"errors\") or (guards.get(\"rc\") and not guards.get(\"refusals\")):", "    if False:"),
    ("models: refused point kept in the stream fit", "resmap_models.py",
     'if point.get("patch") or point["name"] not in summary or refusals(summary, point["name"]):',
     'if point.get("patch") or point["name"] not in summary:'),
    ("models: refused point kept in the processor fit", "resmap_models.py",
     'if point["top"] != "KL_pp_shadow" or point["name"] not in summary or refusals(summary, point["name"]):',
     'if point["top"] != "KL_pp_shadow" or point["name"] not in summary:'),
    ("models: refused point kept in the TDM model", "resmap_models.py",
     'if point["name"] in summary and not refusals(summary, point["name"]):', 'if point["name"] in summary:'),
    ("models: refused anchor kept in the calibration", "resmap_models.py",
     'if name not in summary or "opt" not in data or refusals(summary, name):',
     'if name not in summary or "opt" not in data:'),
    ("models: rank-deficient fit accepted", "resmap_models.py", "    if rank < design.shape[1]:", "    if False:"),
    ("tables: page check reports stale as equal", "resmap_tables.py",
     "stale = text != args.page.read_text()", "stale = False"),
    ("tables: SoC variant fit with fewer than three points", "resmap_tables.py",
     "        if len(present) < 3:", "        if len(present) < 2:"),
    ("sweep: guard refusal lines ignored", "yosys_sweep.py",
     'USER_GUARD = re.compile(r"^%(?:Warning|Error)-USER(?:ERROR|FATAL): (.*)$")', 'USER_GUARD = re.compile(r"^NEVER(.*)$")'),
    ("sweep: summary tie disabled", "yosys_sweep.py",
     "        if tree[\"inclusive\"][top][column] != design[column]:", "        if False:"),
    ("sweep: tracked change read as clean", "yosys_sweep.py",
     'return {"head": head, "clean": not status,', 'return {"head": head, "clean": True,'),
]
for what, name, old, new in OTHER:
    run_mutant(what, name, old, new)

print("== Part 4: wrong figures planted in a copy of the real published map inputs")


def real(what, name, old, new):
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp) / "map"; shutil.copytree(mapdir, t)
        f = t / name; text = f.read_text(); n = text.count(old)
        if n != 1:
            print(f"{what}: SITE NOT FOUND ({n})"); return
        f.write_text(text.replace(old, new, 1))
        r = subprocess.run([sys.executable, "-B", str(d / "resmap_map.py"), "map", str(t)], capture_output=True, text=True)
        out = r.stdout.strip().replace("\n", " | ")
        print(f"{what}: rc {r.returncode}: {out[:400]}")


real("control: unmodified published inputs", "map_utilization.rpt", "| Slice LUTs", "| Slice LUTs")
real("a non-processor leaf's LUT figure 3 -> 5 (KL_mac_rmon_events evt_cdc[3])", "map_hierarchy.rpt",
     "gen_evt_cdc[3].gen_live_lane.evt_cdc                           |                                        cdc_pulse |          3 |          3 |",
     "gen_evt_cdc[3].gen_live_lane.evt_cdc                           |                                        cdc_pulse |          5 |          5 |")
with open(mapdir / "map_cells.tsv") as fh:
    lut = next(l for l in fh if l.startswith("KL_mac_rmon_events/gen_evt_cdc[3]") and "LUT\n" in l and "\tLUT" in l)
cell, prim, level, site, bel = lut.rstrip("\n").split("\t")
letter = bel.split(".")[1][0]
moved = bel.replace(f".{letter}", ".D" if letter != "D" else ".C", 1)
real(f"a census LUT cell moved to another LUT site ({cell.rsplit('/', 1)[-1]} {bel} -> {moved})", "map_cells.tsv",
     lut, lut.replace(bel, moved))
