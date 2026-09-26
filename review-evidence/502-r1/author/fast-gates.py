import os
from pathlib import Path
import subprocess
import sys

os.environ["PATH"] = "/tmp/502-python/bin:" + os.environ["PATH"]
gates = [
 ("nvm-firmware-selftest", ["python3", "sw/firmware/nvm_hosttest/test_nvm_firmware.py", "--self-test"]),
 ("nvm-capture", ["python3", "scripts/check_nvm_capture.py"]),
 ("baremetal", ["python3", "scripts/check_baremetal_only.py", "--check"]),
 ("docs", ["python3", "-B", "scripts/docs_check.py"]),
 ("ci-events", ["python3", "scripts/ci_events.py", "--check"]),
 ("ci-events-selftest", ["python3", "scripts/ci_events.py", "--selftest"]),
 ("em-dash", ["python3", "scripts/check_em_dash.py", "--base", "7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a"]),
 ("doc-style", ["python3", "scripts/check_doc_style.py"]),
 ("toc", ["python3", "scripts/gen_toc.py", "--check"]),
 ("anchors", ["python3", "scripts/gen_toc.py", "--verify-anchors"]),
 ("doc-paths", ["python3", "scripts/check_doc_paths.py"]),
 ("module-matrix", ["python3", "docs/traceability/gen_module_matrix.py", "--check"]),
 ("xvlog", ["python3", "scripts/xvlog_gate.py", "--check"]),
 ("rtl-source-lists", ["python3", "scripts/check_rtl_source_lists.py"]),
 ("sv-idiom", ["python3", "scripts/check_sv_idiom.py"]),
 ("rtl-lint", ["python3", "scripts/lint_rtl.py", "--check"]),
 ("cpp-idiom", ["python3", "scripts/check_cpp_idiom.py"]),
 ("py-idiom", ["python3", "scripts/check_py_idiom.py"]),
 ("port-contracts", ["python3", "scripts/check_port_contracts.py"]),
 ("naming", ["python3", "scripts/measure_naming.py", "--check"]),
 ("test-evidence", ["python3", "scripts/measure_test_evidence.py", "--check"]),
 ("diff-check", ["git", "diff", "--check"]),
]
failed = []
for name, command in gates:
    rc = subprocess.run([sys.executable, "/tmp/502-run-gate.py", name, *command], timeout=21600).returncode
    if rc:
        failed.append((name, rc))
print("FAILED GATES:", failed, flush=True)
sys.exit(bool(failed))
