#!/usr/bin/env python3
"""R466-2 probe: disable each check of syn/resmap/resmap_map.py in a disposable copy and record
whether `--selftest` still passes. Round 1's thirteen mutants are kept with their exact sites (a site
that no longer exists is reported ABSENT, never re-aimed); round 2 adds mutants for the census LUT
tie, its sub-columns, its parent rows, the LUT-site key, the ancestor climb, and the per-column parts
of the record and flat ties. Usage: mutate_map_r2.py <repo> <scratch dir> [jobs]"""
import shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
repo, scratch = Path(sys.argv[1]), Path(sys.argv[2])
jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 8
R1 = {
    "ancestry-additive-off": ("            if delta[column]:\n                failures.append(f\"ancestry: {parent} {column} is",
                              "            if False:\n                failures.append(f\"ancestry: {parent} {column} is"),
    "ancestry-shared-off": ("            if delta[column] > 0:", "            if False:"),
    "partition-off": ("    failures += partition_ties(rows, root, leaves, adjustments)\n", ""),
    "flat-off": ("    for column, value in flat.items():\n        if abs(", "    for column, value in {}.items():\n        if abs("),
    "record-totals-off": ("    for column in (\"LUT\", \"FF\", \"RAMB36\", \"RAMB18\", \"DSP\", \"CARRY4\", \"SLICE\"):\n        if column not in figures:",
                          "    for column in ():\n        if column not in figures:"),
    "record-scopes-off": ("    for scope, recorded in scopes.items():", "    for scope, recorded in {}.items():"),
    "census-leaf-off": ("            if counted != rows[leaf][column]:", "            if False:"),
    "census-total-off": ("        if total != rows[root][column]:\n            failures.append(f\"census",
                         "        if False:\n            failures.append(f\"census"),
    "census-stray-off": ("    if stray:\n", "    if False:\n"),
    "iob-split-off": ("counts[leaf][\"IOB_FF\" if column == \"FF\" and not SLICE_SITE.fullmatch(site) else column] += 1",
                      "counts[leaf][column] += 1"),
    "slice-share-unnormalized": ("            counts[leaf][\"SLICE\"] += number / total", "            counts[leaf][\"SLICE\"] += number"),
    "depth-off": ("    if depth >= requested_depth(report):", "    if False:"),
    "names-sum-off": ("        if sum(entry[column] for entry in by_name.values()) != rows[f\"{root}/@own\"][column]:", "        if False:"),
}
R2 = {
    "census-lut-off": ("            if counted != rows[key][column]:", "            if False:"),
    "census-lut-leaves-only": ("    for key in rows:\n        for column in SHARED:", "    for key in leaves:\n        for column in SHARED:"),
    "census-lut-parents-only": ("    for key in rows:\n        for column in SHARED:",
                                "    for key in [k for k in rows if k not in leaves]:\n        for column in SHARED:"),
    "census-lut-total-column-only": ("        for column in SHARED:\n            counted = len(", "        for column in (\"LUT\",):\n            counted = len("),
    "census-lut-subcolumns-only": ("        for column in SHARED:\n            counted = len(",
                                   "        for column in (\"logic_LUT\", \"LUTRAM\", \"SRL\"):\n            counted = len("),
    "lut-kind-collapsed": ("            for name in (\"LUT\", column):", "            for name in (\"LUT\", \"logic_LUT\"):"),
    "lut-site-key-by-bel": ("sites[node][name].add((site, match.group(1)))", "sites[node][name].add((site, bel))"),
    "lut-no-ancestor-climb": ("            if node == root:\n                break", "            break"),
    "record-carry4-off": ("(\"LUT\", \"FF\", \"RAMB36\", \"RAMB18\", \"DSP\", \"CARRY4\", \"SLICE\"):\n        if column not in figures:",
                          "(\"LUT\", \"FF\", \"RAMB36\", \"RAMB18\", \"DSP\", \"SLICE\"):\n        if column not in figures:"),
    "record-slice-off": ("(\"LUT\", \"FF\", \"RAMB36\", \"RAMB18\", \"DSP\", \"CARRY4\", \"SLICE\"):\n        if column not in figures:",
                         "(\"LUT\", \"FF\", \"RAMB36\", \"RAMB18\", \"DSP\", \"CARRY4\"):\n        if column not in figures:"),
    "flat-slice-off": ("\"Slice LUTs\": \"LUT\", \"Slice Registers\": \"FF\", \"Slice\": \"SLICE\",",
                       "\"Slice LUTs\": \"LUT\", \"Slice Registers\": \"FF\","),
    "flat-lut-only": ("    for column, value in flat.items():\n        if abs(",
                      "    for column, value in {k: v for k, v in flat.items() if k == \"LUT\"}.items():\n        if abs("),
    "census-leaf-ff-only": ("        for column in ADDITIVE:\n            counted = by_leaf", "        for column in (\"FF\",):\n            counted = by_leaf"),
    "census-leaf-no-ff": ("        for column in ADDITIVE:\n            counted = by_leaf",
                          "        for column in (\"RAMB36\", \"RAMB18\", \"DSP\"):\n            counted = by_leaf"),
}


def run(item):
    name, (old, new) = item
    tree = scratch / name
    if tree.exists():
        shutil.rmtree(tree)
    (tree / "syn").mkdir(parents=True)
    shutil.copytree(repo / "syn/resmap", tree / "syn/resmap", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(repo / "syn/ooc", tree / "syn/ooc", ignore=shutil.ignore_patterns("__pycache__"))
    target = tree / "syn/resmap/resmap_map.py"
    text = target.read_text()
    if text.count(old) != 1:
        shutil.rmtree(tree)
        return name, "ABSENT", None, f"mutation site occurs {text.count(old)} times at this head"
    target.write_text(text.replace(old, new))
    proc = subprocess.run([sys.executable, str(target), "--selftest"], capture_output=True, text=True)
    out = (proc.stdout + proc.stderr).strip().splitlines()
    shutil.rmtree(tree)
    failed = [l.split(": ", 1)[1][:110] for l in out if l.startswith("SELF-TEST FAILED")]
    return name, "SURVIVED" if proc.returncode == 0 else "KILLED", proc.returncode, (out[-1] if out else "") + (
        f" | first failed arm: {failed[0]}" if failed else "")


with ThreadPoolExecutor(jobs) as pool:
    results = list(pool.map(run, [*R1.items(), *R2.items()]))
for name, verdict, rc, detail in results:
    tag = "r1" if name in R1 else "r2"
    print(f"{tag} {name:30s} {verdict:8s} rc={rc} {detail}")
for verdict in ("KILLED", "SURVIVED", "ABSENT"):
    print(f"{verdict}: {[n for n, v, _, _ in results if v == verdict]}")
