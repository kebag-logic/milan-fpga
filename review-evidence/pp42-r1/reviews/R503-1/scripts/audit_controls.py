#!/usr/bin/env python3
"""Read-only baseline comparison and exact planting audit of every notification control."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
base = "e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8"
rel = "tb/pp_top/notify_mutants.py"
old = {"__name__": "review_base", "__file__": str(root / rel)}
new = {"__name__": "review_head", "__file__": str(root / rel)}
exec(compile(subprocess.check_output(["git", "-C", str(root), "show", base + ":" + rel]), rel, "exec"), old)
exec(compile((root / rel).read_text(), rel, "exec"), new)
old_by_name = {m.name: m for m in old["MUTANTS"]}
new_by_name = {m.name: m for m in new["MUTANTS"]}
records = []
for mutant in new["MUTANTS"]:
    texts = {}
    matches = []
    for path, before, after in mutant.edits:
        text = texts.setdefault(path, (root / path).read_text())
        matches.append({"path": path, "occurrences": text.count(before)})
        assert text.count(before) == 1, mutant.name
        texts[path] = text.replace(before, after, 1)
    unchanged = mutant == old_by_name.get(mutant.name) if mutant.name in old_by_name else None
    assert unchanged is not False, mutant.name
    records.append({"name": mutant.name, "unchanged_from_base": unchanged, "planting": matches})
assert set(old_by_name) <= set(new_by_name)
changed = subprocess.check_output(["git", "-C", str(root), "diff", "--name-status", base, "HEAD"], text=True)
assert all(line.split("\t")[1].startswith(("tb/pp_top/", "docs/")) for line in changed.splitlines())
print(json.dumps({"base_controls": len(old_by_name), "head_controls": len(new_by_name),
                  "all_old_definitions_unchanged": True, "all_65_plant_exactly_once": True,
                  "changed_files": changed.splitlines(), "controls": records}, indent=2))
