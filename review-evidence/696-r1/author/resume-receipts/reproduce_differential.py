#!/usr/bin/env python3
"""Attribute the frozen differential failure without changing checkout files.

Usage: VERILATOR=<pinned executable> python3 reproduce_differential.py REPO WORK
WORK must be an empty external disk-backed directory. Requires test dependencies.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
work.mkdir(parents=True, exist_ok=False)
compiler = Path(os.environ["VERILATOR"]).resolve()
wrapper = work / "compiler.py"
wrapper.write_text("""#!/usr/bin/env python3
import os
import sys
args = sys.argv[1:]
for i, arg in enumerate(args):
    if arg.endswith('/hdl/ieee1722/maap/KL_maap.sv'):
        args[i] = os.environ['DIFFERENTIAL_RTL']
    if arg == '-j' and i + 1 < len(args):
        args[i + 1] = '2'
os.execv(os.environ['PINNED_COMPILER'], ['verilator', *args])
""")
wrapper.chmod(0o755)
rows = []
for name, revision, expected in (
    ("current", "bb1940966115e61733147b538182a6bccc3f4597", 1),
    ("resume", "bc89c6c1c6289cb286a39406413ebc1c742d7745", 1),
    ("base", "6aa25dec977c6ad78bf4ff6275de47fb81d0c246", 0),
):
    source = work / (name + ".sv")
    source.write_bytes(subprocess.check_output(
        ["git", "show", revision + ":hdl/ieee1722/maap/KL_maap.sv"], cwd=repo))
    env = dict(os.environ, TMPDIR=str(work), PYTHONDONTWRITEBYTECODE="1",
               VERILATOR=str(wrapper), VERILATOR_JOBS="2",
               PINNED_COMPILER=str(compiler), DIFFERENTIAL_RTL=str(source))
    argv = ["python3", "sw/firmware/ctrl/test/maap_differential.py",
            "--keep", str(work / name)]
    if name == "current":
        argv.append("--self-test")
    with (work / (name + ".log")).open("w") as log:
        result = subprocess.run(argv, cwd=repo, env=env, stdout=log,
                                stderr=subprocess.STDOUT, check=False)
    text = (work / (name + ".log")).read_text()
    checks = ("checks: 12   failures: 1" if expected else "checks: 12   failures: 0")
    matched = result.returncode == expected and checks in text
    if expected:
        matched = matched and "actual: 5770 vs 5790" in text
    rows.append(dict(population=name, revision=revision, rc=result.returncode,
                     expected_rc=expected, matched=matched,
                     rtl_sha256=hashlib.sha256(source.read_bytes()).hexdigest()))
    print(name, result.returncode, "matched" if matched else "UNEXPECTED", flush=True)
(work / "results.json").write_text(json.dumps(rows, indent=2) + "\n")
raise SystemExit(0 if all(row["matched"] for row in rows) else 1)
