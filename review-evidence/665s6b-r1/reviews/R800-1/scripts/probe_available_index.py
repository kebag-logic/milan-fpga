#!/usr/bin/env python3
"""probe_available_index.py TREE OUT - the two available_index mutants of TREE's aecp_mutants.py, through its
own campaign (it plants a copy, never TREE), plus an unplanted control of the same arm that must pass.
Exit 0 when both mutants are caught by their named check and the control passes."""
import sys
from pathlib import Path

tree, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / "sw/firmware/ctrl/test"))
import aecp_mutants as am  # noqa: E402

names = ("app-available-index-next", "app-available-index-unguarded")
picked = tuple(d for d in am.DEFECTS if d.name in names)
assert len(picked) == 2, picked
# an unplanted control: a defect whose replacement is its original, which must NOT be caught
control = am.Defect("control-unplanted", picked[0].path, picked[0].old, picked[0].old, picked[0].checks)
am.controls()
am.controls = lambda: None
am.DEFECTS = picked + (control,)
escaped = am.campaign(out, jobs=4, stack=(tree / "third_party/tsn-c-stack").resolve())
import json  # noqa: E402
res = {r["name"]: r["caught"] for r in json.loads((out / "results.json").read_text())}
ok = res[names[0]] and res[names[1]] and not res["control-unplanted"]
print(f"results {res}")
print(f"probe_available_index: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
