#!/usr/bin/env python3
"""Reviewer-chosen faults in the #652 resmap code, each in a disposable copy of
the head; the module's own --selftest must turn red. The copy is restored with
`git checkout` after each probe.
Usage: c10_resmap_mutations.py <tree copy> <receipt file>"""
import json
import subprocess
import sys
from pathlib import Path

TREE, OUT = Path(sys.argv[1]), Path(sys.argv[2])
SWEEP, MODELS, TABLES = "syn/resmap/yosys_sweep.py", "syn/resmap/resmap_models.py", "syn/resmap/resmap_tables.py"
PROBES = [
    ("traceback_read_as_refusal", SWEEP,
     "if rc == 1 and len(refusals) == 1 and not any(line.startswith(\"Traceback\") for line in lines):",
     "if rc == 1 and len(refusals) == 1:"),
    ("any_rc_read_as_refusal", SWEEP, "if rc == 1 and len(refusals) == 1", "if rc != 0 and len(refusals) == 1"),
    ("unrun_variant_taken_as_built", SWEEP,
     "raise PlanError(f\"{point['name']}: shape {shape} has no builder outcome; run the shapes command first\")",
     "return \"\""),
    ("run_prices_refused_point", SWEEP, "        if line:\n            print(f\"point {point['name']}: not priced",
     "        if False:\n            print(f\"point {point['name']}: not priced"),
    ("summary_keeps_priced_refused_receipt", SWEEP,
     "if line and (directory / \"receipt.json\").is_file():", "if False:"),
    ("models_builder_record_ignored", MODELS, "    if builder is not None:\n        return [builder[\"refusal\"]]",
     "    if False:\n        return [builder[\"refusal\"]]"),
    ("tables_refused_by_always_guard", TABLES, "\"builder\" if name in builder else", "\"elaboration guard\" if name in builder else"),
]


def selftest(rel):
    r = subprocess.run(["python3", rel, "--selftest"], cwd=TREE, capture_output=True, text=True, timeout=1800)
    return r.returncode, (r.stdout + r.stderr).strip().splitlines()[-3:]


subprocess.run(["git", "checkout", "--", "."], cwd=TREE, check=True)
results = []
for name, rel, old, new in PROBES:
    p = TREE / rel
    text = p.read_text()
    if text.count(old) != 1:
        results.append({"probe": name, "error": f"anchor occurs {text.count(old)} times"})
        continue
    p.write_text(text.replace(old, new))
    rc, tail = selftest(rel)
    subprocess.run(["git", "checkout", "--", "."], cwd=TREE, check=True)
    results.append({"probe": name, "module": rel, "selftest_rc": rc, "red": rc != 0, "tail": tail})
clean = subprocess.run(["git", "status", "--porcelain"], cwd=TREE, capture_output=True, text=True).stdout == ""
OUT.write_text(json.dumps({"results": results, "restored_clean": clean}, indent=1) + "\n")
print(json.dumps({"red": sum(r.get("red", False) for r in results), "of": len(results), "clean": clean}))
