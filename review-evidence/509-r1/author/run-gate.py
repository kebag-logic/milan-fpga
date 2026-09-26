"""Run one foreground gate with a durable exit status and generous timeout."""

import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path.cwd()
receipts = Path(__file__).resolve().parent
python = "$VALIDATION_STORAGE/509-a327-python/bin/python3"
base = "7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a"
gates = {
    "builder-sdk": [python, str(receipts / "builder-mode.py"), "sdk", "--audit",
                    str(receipts / "compiler-sdk.jsonl")],
    "builder-absent": [python, str(receipts / "builder-mode.py"), "absent", "--audit",
                       str(receipts / "compiler-absent.jsonl")],
    "aem-selftest": [python, "avdecc/gen_aem_store.py", "--self-test"],
    "nvm-firmware": [python, "sw/firmware/nvm_hosttest/test_nvm_firmware.py", "--self-test"],
    "nvm-capture": [python, "scripts/check_nvm_capture.py"],
    "baremetal": [python, "scripts/check_baremetal_only.py", "--check"],
    "docs-git": [python, "-B", "scripts/docs_check.py"],
    "docs-no-git": [python, "-B", "scripts/docs_check.py"],
    "ci-check": [python, "scripts/ci_events.py", "--check"],
    "ci-selftest": [python, "scripts/ci_events.py", "--selftest"],
    "em-dash": [python, "scripts/check_em_dash.py", "--base", base],
    "doc-style": [python, "scripts/check_doc_style.py"],
    "toc": [python, "scripts/gen_toc.py", "--check"],
    "anchors": [python, "scripts/gen_toc.py", "--verify-anchors"],
    "doc-paths": [python, "scripts/check_doc_paths.py"],
    "module-matrix": [python, "docs/traceability/gen_module_matrix.py", "--check"],
    "xvlog": [python, "scripts/xvlog_gate.py", "--check"],
    "rtl-lists": [python, "scripts/check_rtl_source_lists.py"],
    "sv-idiom": [python, "scripts/check_sv_idiom.py"],
    "rtl-lint": [python, "scripts/lint_rtl.py", "--check"],
    "cpp-idiom": [python, "scripts/check_cpp_idiom.py"],
    "py-idiom": [python, "scripts/check_py_idiom.py"],
    "ports": [python, "scripts/check_port_contracts.py"],
    "naming": [python, "scripts/measure_naming.py", "--check"],
    "test-evidence": [python, "scripts/measure_test_evidence.py", "--check"],
    "behave": ["behave", "--no-capture", "-f", "plain"],
    "diff": ["git", "diff", "--check", base],
    "entity-shape": [python, "scripts/check_entity_shape.py", "--self-test"],
    "audit": [python, "scripts/audit_pp_descriptors.py", "--output",
              str(receipts / "descriptor-audit.json")],
}
name = sys.argv[1]
environment = dict(os.environ, PYTHONUNBUFFERED="1")
environment["PATH"] = str(Path(python).parent) + os.pathsep + environment["PATH"]
if name == "docs-no-git":
    environment["GIT_DIR"] = "/dev/null"
cwd = root / "tests" if name == "behave" else root
log = receipts / (name + ".log")
print("START", name, flush=True)
started = time.monotonic()
with log.open("w") as stream:
    result = subprocess.run(gates[name], cwd=cwd, env=environment,
                            stdout=stream, stderr=subprocess.STDOUT, timeout=7200)
row = dict(gate=name, command=gates[name], cwd=str(cwd), exit_code=result.returncode,
           seconds=round(time.monotonic() - started, 2), log=log.name)
with (receipts / "gates.jsonl").open("a") as stream:
    stream.write(json.dumps(row) + "\n")
print(json.dumps(row), flush=True)
raise SystemExit(result.returncode)
