#!/usr/bin/env python3
"""Reviewer planted-defect campaign. Each plant replaces one exact string in one
file of a disposable copy of the head tree, then runs the desc_store gate.
Usage: plant.py <head-tree> <work-dir> <plant-name>   (prints NAME KILLED|SURVIVED|BADPLANT)"""
import sys, shutil, subprocess, pathlib
D = "hdl/aecp/desc/"
PLANTS = {
 # --- lint code ---
 "aaf-source-ge1":        (D+"model_rules.py", "if total != 1:", "if total > 1:"),
 "base-depth-any":        (D+"model_rules.py", "or depth != 32 or", "or"),
 "formats-max-47":        (D+"model_rules.py", "FORMATS_MAX = 46 ", "FORMATS_MAX = 47 "),
 "buffer-off-by-one":     (D+"model_rules.py", "if length is not None and length < BUFFER_MIN_NS:", "if length is not None and length < BUFFER_MIN_NS - 1:"),
 "crf-word-typo":         (D+"model_rules.py", "CRF_MILAN = 0x041060010000BB80", "CRF_MILAN = 0x041060010000BB81"),
 "waiver-ignores-type":   (D+"model_lint.py", "if finding.check != self.check or (cfg, dtype) != self.where[:2]:", "if finding.check != self.check or cfg != self.where[0]:"),
 "waiver-never-stale":    (D+"model_lint.py", "                problems.append(f\"its check passes for {scope}\")", "                pass"),
 "reason-any-text":       (D+"model_lint.py", "if not ISSUE_REF.search(reason):", "if not reason:"),
 "digest-skips-maps":     (D+"model_lint.py", "            for index, body in sorted(model[cfg][dtype].items()):", "            for index, body in sorted(model[cfg][dtype].items() if dtype != 0x17 else ()):"),
 "counts-min-not-max":    (D+"model_rules.py", "most_out = max(len(", "most_out = min(len("),
 "iface-count-only":      (D+"model_rules.py", "if shapes[cfg] != first:", "if len(shapes[cfg]) != len(first):"),
 "unique-per-map":        (D+"model_rules.py", "            for k in range(count):\n                key = struct", "            seen = {}\n            for k in range(count):\n                key = struct"),
 "order-no-control-arm":  (D+"model_rules.py", "if top and owned and max(top) > min(owned):", "if False:"),
 "covers-ut-current":     (D+"model_rules.py", "if entry >> 56 != 0x02 or not entry & up_to or current & up_to:", "if entry >> 56 != 0x02 or not entry & up_to:"),
 "layout-no-length":      (D+"model_rules.py", "    if len(body) != end:\n", "    if False:\n"),
 "identity-allow-dups":   (D+"model_rules.py", "if listed != list(range(count)):", "if sorted(set(listed)) != list(range(count)):"),
 "rate-count-9":          (D+"model_rules.py", "if count > RATES_MAX:", "if count > RATES_MAX + 1:"),
 "model-id-allones-ok":   (D+"model_rules.py", "if model_id in (0, (1 << 64) - 1):", "if model_id == 0:"),
 "cli-writes-first":      (D+"gen_desc_image.py", "    try:\n        img, report = build(", "    open(args.output, 'wb').close()\n    try:\n        img, report = build("),
 "lint-runs-before-layout": (D+"gen_desc_image.py", "    groups = _grouped_descriptors(model)\n    entries = _index_entries(groups, names, line_bytes)", "    groups = _grouped_descriptors(model)\n    _lint_lines(groups, model, lint, (adp, model_ids))\n    entries = _index_entries(groups, names, line_bytes)"),
 "identify-any-config":   (D+"model_rules.py", "common = sorted(set.intersection(*held)) if held else []", "common = sorted(set.union(*held)) if held else []"),
 "single-parent-off":     (D+"model_rules.py", "if len(parents) > 1:", "if len(parents) > 2:"),
 # --- the positive model ---
 "min-buffer-2125999":    (D+"milan_min.json", '"buffer_length",               "size": 4, "value": 2126000},\n        {"name": "redundant_offset",            "size": 2, "value": 146},\n        {"name": "number_of_redundant_streams", "size": 2, "value": 0},\n        {"name": "timing",                      "size": 2, "value": 0},\n        {"name": "formats_0",                   "size": 8, "value": "0x0215', '"buffer_length",               "size": 4, "value": 2125999},\n        {"name": "redundant_offset",            "size": 2, "value": 146},\n        {"name": "number_of_redundant_streams", "size": 2, "value": 0},\n        {"name": "timing",                      "size": 2, "value": 0},\n        {"name": "formats_0",                   "size": 8, "value": "0x0215'),
 "min-cluster-format":    (D+"milan_min.json", '"Output 2"},\n        {"name": "localized_description", "size": 2, "value": "0xFFFF"},\n        {"name": "signal_type",           "size": 2, "value": "0xFFFF"},\n        {"name": "signal_index",          "size": 2, "value": 0},\n        {"name": "signal_output",         "size": 2, "value": 0},\n        {"name": "path_latency",          "size": 4, "value": 0},\n        {"name": "block_latency",         "size": 4, "value": 0},\n        {"name": "channel_count",         "size": 2, "value": 1},\n        {"name": "format",                "size": 1, "value": "0x40"}', '"Output 2"},\n        {"name": "localized_description", "size": 2, "value": "0xFFFF"},\n        {"name": "signal_type",           "size": 2, "value": "0xFFFF"},\n        {"name": "signal_index",          "size": 2, "value": 0},\n        {"name": "signal_output",         "size": 2, "value": 0},\n        {"name": "path_latency",          "size": 4, "value": 0},\n        {"name": "block_latency",         "size": 4, "value": 0},\n        {"name": "channel_count",         "size": 2, "value": 1},\n        {"name": "format",                "size": 1, "value": "0x41"}'),
 "min-talker-sources-2":  (D+"milan_min.json", '"talker_stream_sources",   "size": 2, "value": 1}', '"talker_stream_sources",   "size": 2, "value": 2}'),
 "min-sources-swapped":   (D+"milan_min.json", '"clock_sources_1",       "size": 2, "value": 1}', '"clock_sources_1",       "size": 2, "value": 0}'),
 "min-identify-type":     (D+"milan_min.json", '"control_type",          "size": 8, "value": "0x90E0F00000000001"}', '"control_type",          "size": 8, "value": "0x90E0F00000000002"}'),
 # expected NOT to fail (exclusions): renaming and a new entity_id keep the gate green
 "min-rename-cluster(expect-pass)": (D+"milan_min.json", '"Output 2",', '"Output Two",'),
 "min-new-entity-id(expect-pass)":  (D+"milan_min.json", '"0x020000FFFE00C800"', '"0x020000FFFE00C8FF"'),
}
head, work, name = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
path, old, new = PLANTS[name]
tree = work / name.replace("(", "_").replace(")", "")
if tree.exists(): shutil.rmtree(tree)
shutil.copytree(head / "hdl/aecp/desc", tree / "hdl/aecp/desc"); shutil.copytree(head / "tb/desc_store", tree / "tb/desc_store", ignore=shutil.ignore_patterns("obj_dir"))
f = tree / path; text = f.read_text(encoding="utf-8")
if text.count(old) != 1:
    print(f"{name} BADPLANT (pattern count {text.count(old)})"); sys.exit(0)
f.write_text(text.replace(old, new), encoding="utf-8")
r = subprocess.run([sys.executable, "-B", "test_gen_desc_image.py"], cwd=tree / "tb/desc_store", capture_output=True, text=True, timeout=600)
fails = [l for l in r.stderr.splitlines() if l.startswith(("FAIL:", "ERROR:"))]
print(f"{name} {'KILLED' if r.returncode else 'SURVIVED'} rc={r.returncode} {fails[:3]}")
