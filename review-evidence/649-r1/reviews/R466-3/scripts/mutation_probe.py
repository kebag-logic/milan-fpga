#!/usr/bin/env python3
"""Reviewer mutation probe for #649 (R466-3): apply one source mutant at a time to a scratch archive of the
head under review and run that script's own --selftest; a mutant is KILLED when the self-test exits non-zero.
Usage: mutation_probe.py <repo> <head> <scratch dir> <out json>"""
import concurrent.futures, json, shutil, subprocess, sys, tarfile, io
from pathlib import Path

repo, head, scratch, out = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
M = "syn/resmap/resmap_map.py"; MO = "syn/resmap/resmap_models.py"; T = "syn/resmap/resmap_tables.py"
Y = "syn/resmap/yosys_sweep.py"
MUTANTS = [
 ("map-ancestry-additive-off", M, "            if delta[column]:\n", "            if False:\n"),
 ("map-ancestry-shared-off", M, "            if delta[column] > 0:\n", "            if False:\n"),
 ("map-census-leaf-additive-off", M, "            if counted != rows[leaf][column]:\n", "            if False:\n"),
 ("map-census-lut-leaves-only", M, "    for key in rows:\n        for column in SHARED:", "    for key in leaves:\n        for column in SHARED:"),
 ("map-census-lut-off", M, "            if counted != rows[key][column]:\n", "            if False:\n"),
 ("map-lut-5lut-ignored", M, r'LUT_BEL = re.compile(r"SLICE[LM]\.([A-D])[56]LUT")', r'LUT_BEL = re.compile(r"SLICE[LM]\.([A-D])6LUT")'),
 ("map-lut-kind-all-logic", M, '        for name in ("LUT", column):', '        for name in ("LUT", "logic_LUT"):'),
 ("map-stray-off", M, "    if stray:\n", "    if False:\n"),
 ("map-iob-ff-merged", M, 'counts[leaf]["IOB_FF" if column == "FF" and not SLICE_SITE.fullmatch(site) else column] += 1',
  'counts[leaf][column] += 1'),
 ("map-flat-off", M, "        if abs(top.get(column, -1) - value) > 1e-6:\n            failures.append(f\"flat",
  "        if False:\n            failures.append(f\"flat"),
 ("map-record-totals-off", M, "        elif abs(top.get(column, -1) - figures[column]) > 1e-6:", "        elif False:"),
 ("map-record-scopes-off", M, "            if mine.get(column) != value:", "            if False:"),
 ("map-depth-boundary", M, "    if depth >= requested_depth(report):", "    if depth > requested_depth(report):"),
 ("map-depth-off", M, "    if depth >= requested_depth(report):", "    if False:"),
 ("map-owner-shallowest", M, "    for cut in range(len(parts), -1, -1):", "    for cut in range(0, len(parts) + 1):"),
 ("map-slice-equal-split", M, "            counts[leaf][\"SLICE\"] += number / total", "            counts[leaf][\"SLICE\"] += 1 / len(site_cells)"),
 ("models-missing-record-clean", MO, "    if guards is None:\n        raise GuardError", "    if guards is None:\n        return []\n        raise GuardError"),
 ("models-hard-error-clean", MO, "    if guards.get(\"errors\") or (guards.get(\"rc\") and not guards.get(\"refusals\")):",
  "    if False:"),
 ("models-stream-keeps-refused", MO, "        if point.get(\"patch\") or point[\"name\"] not in summary or refusals(summary, point[\"name\"]):",
  "        if point.get(\"patch\") or point[\"name\"] not in summary:"),
 ("models-param-keeps-refused", MO, "        if point[\"top\"] != \"KL_pp_shadow\" or point[\"name\"] not in summary or refusals(summary, point[\"name\"]):",
  "        if point[\"top\"] != \"KL_pp_shadow\" or point[\"name\"] not in summary:"),
 ("models-tdm-keeps-refused", MO, "        if point[\"name\"] in summary and not refusals(summary, point[\"name\"]):",
  "        if point[\"name\"] in summary:"),
 ("models-calibration-keeps-refused", MO, "        if name not in summary or \"opt\" not in data or refusals(summary, name):",
  "        if name not in summary or \"opt\" not in data:"),
 ("models-rank-check-off", MO, "    if rank < design.shape[1]:", "    if False:"),
 ("models-vivado-depth-off-by-one", MO, "        depth = (indent - 1) // 2", "        depth = indent // 2"),
 ("tables-page-check-always-equal", T, "    stale = text != args.page.read_text()", "    stale = False"),
 ("tables-page-missing-ignored", T, "    if missing:\n        print(f\"page: no generated table", "    if False:\n        print(f\"page: no generated table"),
 ("tables-soc-change-sign", T, "*(signed(total[m] - ship[m], 1 if m == \"BRAM\" else 0) for m in MEASURES)",
  "*(signed(ship[m] - total[m], 1 if m == \"BRAM\" else 0) for m in MEASURES)"),
 ("tables-soc-two-point-fit", T, "        if len(present) < 3:", "        if len(present) < 2:"),
 ("sweep-tie-off", Y, "        if tree[\"inclusive\"][top][column] != design[column]:", "        if False:"),
 ("sweep-guard-hard-error-missed", Y, 'HARD_ERROR = re.compile(r"^%Error(?!-USER)(?!: Exiting due to)")', 'HARD_ERROR = re.compile(r"^%Error-NEVER")'),
 ("sweep-require-clean-noop", Y, "    if not state[\"clean\"]:\n        raise PlanError", "    if False:\n        raise PlanError"),
 ("sweep-lutram-cost-zero", Y, "            out[\"LUTRAM\"] += count * LUTRAM_COST[kind]", "            out[\"LUTRAM\"] += 0"),
]

def base_tree() -> Path:
    tree = scratch / "base"
    if not tree.exists():
        tree.mkdir(parents=True)
        data = subprocess.run(["git", "-C", repo, "archive", head], capture_output=True, check=True).stdout
        tarfile.open(fileobj=io.BytesIO(data)).extractall(tree, filter="tar")
    return tree

def run(mutant):
    name, path, old, new = mutant
    tree = scratch / name
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(base_tree(), tree, symlinks=True)
    target = tree / path
    text = target.read_text()
    if text.count(old) != 1:
        return {"mutant": name, "file": path, "status": "NOT APPLIED", "count": text.count(old)}
    target.write_text(text.replace(old, new))
    r = subprocess.run([sys.executable, path, "--selftest"], cwd=tree, capture_output=True, text=True,
                       env={"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin"}, timeout=300)
    last = (r.stdout.strip().splitlines() or [""])[-1]
    shutil.rmtree(tree)
    return {"mutant": name, "file": path, "status": "KILLED" if r.returncode else "SURVIVED", "rc": r.returncode,
            "last_line": last}

base_tree()
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
    results = list(pool.map(run, MUTANTS))
clean = subprocess.run
out.write_text(json.dumps({"head": head, "results": results}, indent=1) + "\n")
for r in results:
    print(f"{r['status']:12} {r['mutant']:36} {r.get('last_line', r.get('count'))}")
