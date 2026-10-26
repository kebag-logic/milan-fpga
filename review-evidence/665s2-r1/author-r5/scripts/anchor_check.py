#!/usr/bin/env python3
"""Count each reviewer mutant's exact-text anchor in a harness directory: a mutant whose anchor
is not unique is reported, not run, by the reviewer's script, so every anchor must stay unique.
Reads both forms: a list of (id, file, old, new, what) and a dict {name: (file, old, new)}.
Usage: anchor_check.py HARNESS_DIR SCRIPT..."""
import importlib.util
import sys
from pathlib import Path

harness = Path(sys.argv[1])
scripts = sys.argv[2:]
bad = 0
for script in scripts:
    # A probe script reads its checkout and output from argv at import; neither is used here.
    sys.argv = [script, str(harness.parents[2]), '/nonexistent']
    spec = importlib.util.spec_from_file_location(Path(script).stem, script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    mutants = module.MUTANTS
    rows = ([(name, *v) for name, v in mutants.items()] if isinstance(mutants, dict)
            else [m[:4] for m in mutants])
    for ident, name, old, _new in rows:
        n = (harness / name).read_text().count(old)
        bad += n != 1
        print(f'{Path(script).name} {ident.split(" ")[0]} {name} anchors={n} {"ok" if n == 1 else "NOT UNIQUE"}')
print(f'anchor check: {bad} not unique')
raise SystemExit(1 if bad else 0)
