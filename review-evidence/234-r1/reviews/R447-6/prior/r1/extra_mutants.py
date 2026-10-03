#!/usr/bin/env python3
"""Reviewer mutants for syn/ooc/pp_resource_gate.py beyond the shipped 25.

Usage: extra_mutants.py <repo checkout> <scratch dir>
Each mutant edits exactly one unique line of a copy of the gate and runs the
shipped self-test against it (the same harness shape as the shipped campaign).
A mutant the self-test still passes is reported SURVIVED. The script never
writes inside the checkout. Exit 0 always; the tally is the result.
"""
import ast
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import shutil
import subprocess
import sys

MUTANTS = {
    # disabled checks: a gated figure removed from the gated set
    "ooc RAMB36 not gated": ('"ooc": ("LUT", "FF", "RAMB36", "RAMB18", "DSP")}',
                             '"ooc": ("LUT", "FF", "RAMB18", "DSP")}'),
    "ooc DSP not gated": ('"ooc": ("LUT", "FF", "RAMB36", "RAMB18", "DSP")}',
                          '"ooc": ("LUT", "FF", "RAMB36", "RAMB18")}'),
    "route DSP not gated": ('GATED = {"route": ("LUT", "FF", "SLICE", "RAMB36", "RAMB18", "DSP", "WNS_ns", "WHS_ns"),',
                            'GATED = {"route": ("LUT", "FF", "SLICE", "RAMB36", "RAMB18", "WNS_ns", "WHS_ns"),'),
    "route RAMB36 not gated": ('GATED = {"route": ("LUT", "FF", "SLICE", "RAMB36", "RAMB18", "DSP", "WNS_ns", "WHS_ns"),',
                               'GATED = {"route": ("LUT", "FF", "SLICE", "RAMB18", "DSP", "WNS_ns", "WHS_ns"),'),
    # the CLI exit for an unreadable or not-comparable measurement
    "CLI refusal exits 0": ('        print(f"NOT COMPARABLE: {error}")\n        return 2\n',
                            '        print(f"NOT COMPARABLE: {error}")\n        return 0\n'),
    "CLI check-baseline exits 0": ('        return 2 if problems else 0\n', '        return 0\n'),
    # identity fields no arm moves
    "design state not bound": ('"state": header(report, "Design State"),', '"state": "x",'),
    "design name not bound": ('"design": header(report, "Design"),', '"design": "x",'),
    "header uniqueness": ("    if len(hits) != 1:\n", "    if not hits:\n"),
    # boundaries
    "ceiling boundary": ('        if candidate["figures"][figure] > ceiling:\n',
                         '        if candidate["figures"][figure] >= ceiling:\n'),
    "floor boundary": ("        if after < floor:\n", "        if after <= floor:\n"),
    "timing fall boundary": ("        if before - after > tolerance:\n", "        if before - after >= tolerance:\n"),
    # parser guards
    "one timing summary": ("    if len(blocks) != 2:\n", "    if len(blocks) < 2:\n"),
    "timing header present": ("    if heads is None or heads + 2 >= len(lines):\n", "    if heads is None:\n"),
    "one generated top": ("    if len(generated) != 1 or len(repository) != 1:\n", "    if False:\n"),
    "include dir present": ("            if not folder.is_dir():\n", "            if False:\n"),
    "baseline floor value": ("            elif figure in TIMING and figures[figure] < entry[\"floor\"][figure]:\n",
                             "            elif False:\n"),
    "candidate kind from directory": ("        candidate = record(directory, kind_of(directory))\n",
                                      "        candidate = record(directory, \"route\")\n"),
}


def run(name, change, source, here, tmp):
    old, new = change
    if source.count(old) != 1:
        return name, "NOT-UNIQUE", ""
    changed = source.replace(old, new)
    ast.parse(changed)
    folder = tmp / name.replace(" ", "_")
    folder.mkdir()
    for sibling in ("pp_baseline_rank.py", "pp_resource_gate_selftest.py"):
        shutil.copy2(here / sibling, folder / sibling)
    (folder / "pp_resource_gate.py").write_text(changed)
    result = subprocess.run([sys.executable, "-B", str(folder / "pp_resource_gate.py"), "--selftest"],
                            capture_output=True, text=True, timeout=300, cwd=folder)
    tail = (result.stdout + result.stderr).strip().splitlines()[-1:] or [""]
    return name, "KILLED" if result.returncode else "SURVIVED", f"rc={result.returncode} {tail[0][:160]}"


def main():
    here = Path(sys.argv[1]) / "syn/ooc"
    tmp = Path(sys.argv[2]).resolve()
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    source = (here / "pp_resource_gate.py").read_text()
    control = run("control", ("BASELINE = ", "BASELINE = "), source, here, tmp)
    print(f"control: {'PASS' if control[1] == 'SURVIVED' else 'FAIL'} {control[2]}")
    if control[1] != "SURVIVED":
        sys.exit("the unmutated control must pass the self-test")
    with ThreadPoolExecutor(max_workers=16) as pool:
        results = list(pool.map(lambda item: run(item[0], item[1], source, here, tmp), MUTANTS.items()))
    for name, verdict, detail in results:
        print(f"{verdict:<10} {name}: {detail}")
    print(f"extra mutants: {sum(v == 'KILLED' for _, v, _ in results)} killed, "
          f"{sum(v == 'SURVIVED' for _, v, _ in results)} survived, "
          f"{sum(v == 'NOT-UNIQUE' for _, v, _ in results)} not unique, of {len(results)}")


if __name__ == "__main__":
    main()
