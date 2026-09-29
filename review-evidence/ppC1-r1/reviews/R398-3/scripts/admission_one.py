#!/usr/bin/env python3
"""Run one (variant, suite) cell of tb/srp_admission/mutants.py with the driver's own
tables and judge, in a private tree. usage: admission_one.py <repo> <outdir> <label> <suite-name>
<label> is 'control' or a MUTANTS label; <suite-name> is a SUITES name (e.g. srp-top)."""
import importlib.util
import sys
import tempfile
from pathlib import Path

repo, out, label, sname = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3], sys.argv[4]
spec = importlib.util.spec_from_file_location("adm", repo / "tb/srp_admission/mutants.py")
adm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adm)
out.mkdir(parents=True, exist_ok=True)
original = (repo / adm.ADMISSION).read_text()
source, expects = original, {}
if label != "control":
    edits, expects = next((e, x) for lab, e, x in adm.MUTANTS if lab == label)
    for anchor, replacement, count in edits:
        assert source.count(anchor) == count, anchor
        source = source.replace(anchor, replacement)
name, suite, command = next(s for s in adm.SUITES if s[0] == sname)
with tempfile.TemporaryDirectory(prefix="adm-one-", dir=out) as tmp:
    tree = Path(tmp)
    adm.build_tree(tree)
    (tree / adm.ADMISSION).write_text(source)
    status, contents = adm.run_suite(tree, suite, command, out / f"{label}-{name}.log")
ok = adm.judge(expects.get(suite) if expects else None, status, contents)
print(f"{label} {name}: rc={status} {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
