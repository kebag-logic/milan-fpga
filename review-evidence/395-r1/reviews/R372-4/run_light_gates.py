#!/usr/bin/env python3
"""R372-4: serial, foreground light gates at the merge head (no builder bank, no Vivado).

Usage: python3 -B run_light_gates.py <repo-root> <markdown-python> <litex-python> <packet-dir>
Writes receipts/gates/<name>.log and receipts/light-gates.json under the packet.
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

root, md, litex, packet = (Path(a) for a in sys.argv[1:5])
HEAD = "895be30712acf8dd80956a5b954690859b080d87"
BASE, DEV, BRANCH = ("8bc97021f28fb7f729418d3a00851c84ea0b50fd",
                     "1fa2357fcb9b83ad7d6cbeab0c7cc0eb957cdd3a",
                     "3b5603e3d16a164c35329efeb633800fe4fe9f95")
logs = packet / "receipts/gates"
logs.mkdir(parents=True, exist_ok=True)
scratch = packet / "scratch/report-gen"
scratch.mkdir(parents=True, exist_ok=True)
dummy = scratch / "input/dummy_route.dcp"
dummy.parent.mkdir(exist_ok=True)
dummy.write_bytes(b"not a checkpoint; script generation only\n")
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", PYTHONUNBUFFERED="1")
py = sys.executable
gates = [
    ("ci-scope-selftest", [py, "-B", "scripts/ci_scope.py", "--selftest"]),
    ("docs", [md, "-B", "scripts/docs_check.py"]),
    ("doc-paths", [md, "-B", "scripts/check_doc_paths.py"]),
    ("toc", [md, "-B", "scripts/gen_toc.py", "--check"]),
    ("em-dash-vs-base", [md, "-B", "scripts/check_em_dash.py", "--base", BASE]),
    ("em-dash-vs-dev", [md, "-B", "scripts/check_em_dash.py", "--base", DEV]),
    ("feature-status", [py, "-B", "scripts/check_feature_status.py", "--self-test"]),
    ("doc-style", [py, "-B", "scripts/check_doc_style.py"]),
    ("doc-style-selftest", [py, "-B", "scripts/check_doc_style.py", "--selftest"]),
    ("solution-docs", [py, "-B", "scripts/check_solution_docs.py"]),
    ("python-idiom", [py, "-B", "scripts/check_py_idiom.py"]),
    ("python-idiom-selftest", [py, "-B", "scripts/check_py_idiom.py", "--selftest"]),
    ("baremetal-only-check", [py, "-B", "scripts/check_baremetal_only.py", "--check"]),
    ("baremetal-only-selftest", [py, "-B", "scripts/check_baremetal_only.py", "--selftest"]),
    ("diff-check-vs-base", ["git", "diff", "--check", BASE, HEAD]),
    ("diff-check-vs-dev", ["git", "diff", "--check", DEV, HEAD]),
    ("diff-check-vs-branch", ["git", "diff", "--check", BRANCH, HEAD]),
    ("report-script-generation", [litex, "-B", "sw/litex/report_timing_grade.py",
                                  str(dummy), str(scratch / "out")]),
]
results = []
for name, argv in gates:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    assert head == HEAD, head
    cwd = root / "sw/litex" if name == "report-script-generation" else root
    if name == "report-script-generation":
        argv = [argv[0], argv[1], "report_timing_grade.py", *argv[3:]]
    log = logs / f"{name}.log"
    start = time.monotonic()
    with log.open("w") as stream:
        rc = subprocess.run(["timeout", "--foreground", "900", *argv], cwd=cwd, env=env,
                            stdout=stream, stderr=subprocess.STDOUT, check=False).returncode
    digest = hashlib.sha256(log.read_bytes()).hexdigest()
    results.append(dict(gate=name, head=HEAD, argv=[str(a).replace(str(root), "<repo>").replace(str(packet), "<packet>")
                                                    for a in argv],
                        returncode=rc, seconds=round(time.monotonic() - start, 2),
                        log=str(log.relative_to(packet)), sha256=digest))
    print(f"{name}: rc={rc} {results[-1]['seconds']}s", flush=True)
if (scratch / "out/report.tcl").is_file():
    (logs / "report-script-generated.tcl").write_text(
        (scratch / "out/report.tcl").read_text().replace(str(packet), "<packet>").replace(str(root), "<repo>"))
(packet / "receipts/light-gates.json").write_text(json.dumps(results, indent=2) + "\n")
bad = [r["gate"] for r in results if r["returncode"]]
print("ALL RC 0" if not bad else f"NONZERO: {bad}")
sys.exit(1 if bad else 0)
