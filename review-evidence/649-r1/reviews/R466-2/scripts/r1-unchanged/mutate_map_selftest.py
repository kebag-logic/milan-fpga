#!/usr/bin/env python3
"""R466 probe: disable each tie of syn/resmap/resmap_map.py in a disposable copy and
record whether `--selftest` still passes. A mutant the self-test does not kill is a
tie the self-test does not exercise. Usage: mutate_map_selftest.py <repo> <scratch dir>"""
import shutil, subprocess, sys
from pathlib import Path
repo, scratch = Path(sys.argv[1]), Path(sys.argv[2])
MUTANTS = {
    "ancestry-additive-off": ("            if delta[column]:\n                failures.append(f\"ancestry: {parent} {column} is",
                              "            if False:\n                failures.append(f\"ancestry: {parent} {column} is"),
    "ancestry-shared-off": ("            if delta[column] > 0:", "            if False:"),
    "partition-off": ("    failures += partition_ties(rows, root, leaves, adjustments)\n", ""),
    "flat-off": ("    for column, value in flat.items():\n        if abs(", "    for column, value in {}.items():\n        if abs("),
    "record-totals-off": ("    for column in (\"LUT\", \"FF\", \"RAMB36\", \"RAMB18\", \"DSP\", \"CARRY4\", \"SLICE\"):\n        if column not in figures:",
                          "    for column in ():\n        if column not in figures:"),
    "record-scopes-off": ("    for scope, recorded in scopes.items():", "    for scope, recorded in {}.items():"),
    "census-leaf-off": ("            if counted != rows[leaf][column]:", "            if False:"),
    "census-total-off": ("        if total != rows[root][column]:\n            failures.append(f\"census:",
                         "        if False:\n            failures.append(f\"census:"),
    "census-stray-off": ("    if stray:\n", "    if False:\n"),
    "iob-split-off": ("counts[leaf][\"IOB_FF\" if column == \"FF\" and not SLICE_SITE.fullmatch(site) else column] += 1",
                      "counts[leaf][column] += 1"),
    "slice-share-unnormalized": ("            counts[leaf][\"SLICE\"] += number / total", "            counts[leaf][\"SLICE\"] += number"),
    "depth-off": ("    if depth >= requested_depth(report):", "    if False:"),
    "names-sum-off": ("        if sum(entry[column] for entry in by_name.values()) != rows[f\"{root}/@own\"][column]:", "        if False:"),
}
results = {}
for name, (old, new) in MUTANTS.items():
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
    run = subprocess.run([sys.executable, str(target), "--selftest"], capture_output=True, text=True)
    last = (run.stdout + run.stderr).strip().splitlines()[-1] if (run.stdout + run.stderr).strip() else ""
    results[name] = ("SURVIVED" if run.returncode == 0 else "KILLED", run.returncode, last[:160])
    print(f"{name:28s} {results[name][0]:8s} rc={run.returncode} {last[:150]}")
    shutil.rmtree(tree)
print("survivors:", [n for n, r in results.items() if r[0] == "SURVIVED"])
