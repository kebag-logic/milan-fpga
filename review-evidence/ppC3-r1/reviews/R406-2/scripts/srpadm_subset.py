#!/usr/bin/env python3
"""Run one (variant, suite) step of tb/srp_admission/mutants.py with the driver's own
MUTANTS, build_tree(), run_suite() and judge() (the driver has no --only and runs past
one call's limit). usage: srpadm_subset.py <tree> <output> <label|control> <suite-name>"""
import importlib.util, sys, tempfile
from pathlib import Path
root, output, label, want = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3], sys.argv[4]
spec = importlib.util.spec_from_file_location("adm", root / "tb/srp_admission/mutants.py")
adm = importlib.util.module_from_spec(spec); spec.loader.exec_module(adm)
output.mkdir(parents=True, exist_ok=True)
original = (adm.REPO / adm.ADMISSION).read_text()
source, expects = original, {}
for lab, edits, exp in adm.MUTANTS:
    if lab == label:
        for anchor, replacement, count in edits:
            if source.count(anchor) != count:
                raise RuntimeError(f"{lab}: expected {count} copies of {anchor!r}")
            source = source.replace(anchor, replacement)
        expects = exp
assert label == "control" or expects, label
with tempfile.TemporaryDirectory(prefix="pp112-subset-") as tmp:
    tree = Path(tmp); adm.build_tree(tree)
    (tree / adm.ADMISSION).write_text(source)
    for name, suite, command in adm.SUITES:
        if name != want: continue
        expect = expects.get(suite) if expects else None
        status, contents = adm.run_suite(tree, suite, command, output / f"{label}-{name}.log")
        ok = adm.judge(expect, status, contents)
        print(f"{label} {name}: rc={status} {'PASS' if ok else 'FAIL'}", flush=True)
        raise SystemExit(0 if ok else 1)
raise SystemExit(f"no suite {want}")
