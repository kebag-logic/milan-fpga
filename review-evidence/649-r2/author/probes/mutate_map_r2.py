#!/usr/bin/env python3
"""Scratch probe (issue #649 round 2): disable each check of syn/resmap/resmap_map.py in a
disposable copy and record whether --selftest still passes. Every check the module docstring
calls a tie must be KILLED; the two bookkeeping guards it says are implied (census totals,
names sum) are expected to survive. Usage: mutate_map_r2.py <repo> <scratch dir>"""
import shutil, subprocess, sys
from pathlib import Path
repo, scratch = Path(sys.argv[1]), Path(sys.argv[2])
TIES = {
    "ancestry-additive-off": ('            if delta[column]:\n                failures.append(f"ancestry: {parent} {column} is',
                              '            if False:\n                failures.append(f"ancestry: {parent} {column} is'),
    "ancestry-shared-off": ("            if delta[column] > 0:", "            if False:"),
    "census-leaf-off": ("            if counted != rows[leaf][column]:", "            if False:"),
    "census-lut-off": ("            if counted != rows[key][column]:", "            if False:"),
    "census-lut-kinds-merged": ('            for name in ("LUT", column):', '            for name in ("LUT", "logic_LUT"):'),
    "census-stray-off": ("    if stray:\n", "    if False:\n"),
    "census-iob-split-off": ('counts[leaf]["IOB_FF" if column == "FF" and not SLICE_SITE.fullmatch(site) else column] += 1',
                             "counts[leaf][column] += 1"),
    "flat-off": ("    for column, value in flat.items():\n        if abs(", "    for column, value in {}.items():\n        if abs("),
    "record-totals-off": ('    for column in ("LUT", "FF", "RAMB36", "RAMB18", "DSP", "CARRY4", "SLICE"):\n        if column not in figures:',
                          "    for column in ():\n        if column not in figures:"),
    "record-scopes-off": ("    for scope, recorded in scopes.items():", "    for scope, recorded in {}.items():"),
    "slice-share-unnormalized": ('            counts[leaf]["SLICE"] += number / total', '            counts[leaf]["SLICE"] += number'),
    "depth-off": ("    if depth >= requested_depth(report):", "    if False:"),
}
GUARDS = {
    "census-totals-off": ("        if total != rows[root][column]:\n            failures.append(f\"census totals:",
                          "        if False:\n            failures.append(f\"census totals:"),
    "names-sum-off": ('        if sum(entry[column] for entry in by_name.values()) != rows[f"{root}/@own"][column]:', "        if False:"),
}
results = {}
for kind, mutants in (("tie", TIES), ("guard", GUARDS)):
    for name, (old, new) in mutants.items():
        tree = scratch / name
        if tree.exists():
            shutil.rmtree(tree)
        (tree / "syn").mkdir(parents=True)
        shutil.copytree(repo / "syn/resmap", tree / "syn/resmap")
        shutil.copytree(repo / "syn/ooc", tree / "syn/ooc")
        target = tree / "syn/resmap/resmap_map.py"
        text = target.read_text()
        assert text.count(old) == 1, f"{name}: mutation site not unique ({text.count(old)})"
        target.write_text(text.replace(old, new))
        run = subprocess.run([sys.executable, "-B", str(target), "--selftest"], capture_output=True, text=True)
        last = (run.stdout + run.stderr).strip().splitlines()[-1] if (run.stdout + run.stderr).strip() else ""
        results[name] = (kind, "SURVIVED" if run.returncode == 0 else "KILLED")
        print(f"{kind:5s} {name:26s} {results[name][1]:8s} rc={run.returncode} {last[:120]}")
        shutil.rmtree(tree)
bad = [n for n, (k, r) in results.items() if (k == "tie") != (r == "KILLED")]
print("tie mutants killed:", sum(1 for k, r in results.values() if k == "tie" and r == "KILLED"), "of", len(TIES))
print("guard mutants surviving (implied, not ties):", sum(1 for k, r in results.values() if k == "guard" and r == "SURVIVED"), "of", len(GUARDS))
print("UNEXPECTED:", bad if bad else "none")
sys.exit(1 if bad else 0)
