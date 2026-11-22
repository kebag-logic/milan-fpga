#!/usr/bin/env python3
"""plants3.py: the round's planted defects in the clone it runs in (cwd), each restored after: the resource sweep's
self-test arms (round 2's three, R879-2-S1's wiring mutants M1-M4) and the harness argv check's two. Controls first."""
import subprocess
from pathlib import Path
HARNESS = ["python3", "-B", "-c", "import sys; sys.path.insert(0, 'tb/verilator/ctrl_service_budget'); import selftest; r = selftest.build_checks(); [print(('PASS ' if ok else 'FAIL ') + n + ('' if ok else ': ' + d)) for n, ok, d in r]; sys.exit(not all(ok for _, ok, _ in r))"]
SOC = ["python3", "-B", "syn/resmap/soc_sweep.py", "--selftest"]
SW = "syn/resmap/soc_sweep.py"
plants = [
 ("R880-1-F1: the plan prices the split SoC", "syn/resmap/sweep_plan.json", '"placement": "all-fabric"', '"placement": "split"', SOC),
 ("R880-1-F1: the soc section names no placement", "syn/resmap/sweep_plan.json", '  "placement": "all-fabric",\n', '', SOC),
 ("R880-1-F1: missing_images reports nothing", SW, '    return [path for path in named if not (tree / path).is_file()]', '    return []', SOC),
 ("R879-2-S1 M1: prepare stops passing --placement to the builder", SW,
  '"-o", str(out), str(config),\n                    "--placement", placement], cwd=tree', '"-o", str(out), str(config)], cwd=tree', SOC),
 ("R879-2-S1 M2: prepare never refuses a missing image", SW, "    if missing:\n        raise yosys_sweep.PlanError(", "    if False:\n        raise yosys_sweep.PlanError(", SOC),
 ("R879-2-S1 M3: command_export asks for the split whatever the plan names", SW,
  "    base = prepare(work, plan_placement(plan))", '    base = prepare(work, "split")', SOC),
 ("R879-2-S1 M4: missing_images reads paths against the wrong root", SW,
  "if not (tree / path).is_file()]", 'if not (Path("/nonexistent") / path).is_file()]', SOC),
 ("R879-S1: split_argv appends a second image pair (the pre-fix behaviour)", "tb/verilator/ctrl_service_budget/build.py",
  "    return [*kept, '--ctrl-mailbox', '--ctrl-firmware', str(elf)]", "    return [*argv, '--ctrl-mailbox', '--ctrl-firmware', str(elf)]", HARNESS),
 ("R879-S1: split_argv keeps the config's image and drops the harness's", "tb/verilator/ctrl_service_budget/build.py",
  "    return [*kept, '--ctrl-mailbox', '--ctrl-firmware', str(elf)]", "    return list(argv)", HARNESS),
]
head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
print(f"# the round's planted defects at {head}, each in this clone, restored after; caught = nonzero exit and a FAIL line")
for cmd in (SOC, HARNESS):
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(f"== control (nothing planted): {' '.join(cmd[:4])}: exit {r.returncode} ({'PASS' if r.returncode == 0 else 'FAILS UNPLANTED'})")
caught = 0
for label, path, old, new, cmd in plants:
    p = Path(path); orig = p.read_text()
    assert orig.count(old) == 1, label
    p.write_text(orig.replace(old, new))
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
    finally:
        p.write_text(orig)
    fails = [l for l in (r.stdout + r.stderr).splitlines() if "FAIL" in l]
    ok = r.returncode != 0 and bool(fails)
    caught += ok
    print(f"== {label}\n   planted in {path}; exit {r.returncode} ({'CAUGHT' if ok else 'MISSED'})")
    for l in fails[:3]:
        print(f"   {l[:300]}")
dirty = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout
print(f"plants caught: {caught} of {len(plants)}; tree after the plants: {len(dirty.splitlines())} changed paths")
