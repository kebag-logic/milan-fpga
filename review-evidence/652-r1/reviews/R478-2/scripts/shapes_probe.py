#!/usr/bin/env python3
"""Run `yosys_sweep.py shapes` from the review clone against a reused export,
with an optional defect planted IN MEMORY (OLD -> NEW, exactly one occurrence)
and a given plan. The clone's files are never written.
Usage: shapes_probe.py <yosys_sweep.py> <plan.json> <work> [OLD NEW]"""
import importlib.util
import sys
from pathlib import Path

path, plan, work = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3]
source = path.read_text(encoding="utf-8")
if len(sys.argv) > 4:
    old, new = (a.encode().decode("unicode_escape") for a in sys.argv[4:6])
    assert source.count(old) == 1, "anchor not unique"
    source = source.replace(old, new)
sys.path.insert(0, str(path.parent))
spec = importlib.util.spec_from_file_location(path.stem, path)
module = importlib.util.module_from_spec(spec)
sys.modules[path.stem] = module
exec(compile(source, str(path), "exec"), module.__dict__)
sys.argv = [str(path), "--plan", plan, "--work", work, "shapes"]
rc = module.main()
print(f"SHAPES rc={rc}")
