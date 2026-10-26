#!/usr/bin/env python3
"""Count each reviewer mutant's exact-text anchor in a harness directory: a mutant whose anchor
is not unique is reported, not run, by the reviewer's script, so every anchor must stay unique.
Usage: anchor_check.py HARNESS_DIR SCRIPT..."""
import importlib.util
import sys
from pathlib import Path

harness = Path(sys.argv[1])
bad = 0
for script in sys.argv[2:]:
    spec = importlib.util.spec_from_file_location(Path(script).stem, script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for ident, name, old, _new, what in module.MUTANTS:
        n = (harness / name).read_text().count(old)
        bad += n != 1
        print(f'{Path(script).name} {ident} {name} anchors={n} {"ok" if n == 1 else "NOT UNIQUE"} {what}')
print(f'anchor check: {bad} not unique')
raise SystemExit(1 if bad else 0)
