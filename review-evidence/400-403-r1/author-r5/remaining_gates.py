"""Run the requested foreground gates sequentially, stopping on failure."""
from pathlib import Path
import subprocess
import sys

scratch = Path("$VALIDATION_STORAGE/400-403-a322")
markdown_python = str(scratch / "markdown-env/bin/python3")
gates = [
    ("builder-absent", ["python3", str(scratch / "full_builder.py"), "absent"]),
    ("declarations", ["python3", "sw/builder/test_declarations.py"]),
    ("firmware", ["python3", "sw/firmware/nvm_hosttest/test_nvm_firmware.py", "--self-test"]),
    ("csr", ["make", "-C", "tb/verilator/csr"]),
    ("pp-shadow", ["make", "-C", "tb/verilator/pp_shadow"]),
    ("baremetal", ["python3", "scripts/check_baremetal_only.py", "--check"]),
    ("docs-git", ["python3", "-B", "scripts/docs_check.py"]),
    ("em-dash", [markdown_python, "scripts/check_em_dash.py", "--base",
                 "5c78ce2e9d831e588e759b696ed549804327e4d8"]),
    ("doc-style", ["python3", "scripts/check_doc_style.py"]),
    ("toc", [markdown_python, "scripts/gen_toc.py", "--check"]),
    ("anchors", [markdown_python, "scripts/gen_toc.py", "--verify-anchors"]),
    ("doc-paths", ["python3", "scripts/check_doc_paths.py"]),
    ("py-idiom", ["python3", "scripts/check_py_idiom.py"]),
    ("test-evidence", ["python3", "scripts/measure_test_evidence.py", "--check"]),
    ("diff-check", ["git", "diff", "--check"]),
    ("committed-diff-check", ["git", "diff", "--check", "e122f3302cf8a8e89de960233a8638b9dd1387dc", "HEAD"]),
    ("stale-text", ["python3", str(scratch / "check_stale.py")]),
    ("artifact-diff", ["diff", "-r", str(scratch / "before"), str(scratch / "after")]),
    ("csr-dry-run", ["make", "-n", "-C", "tb/verilator/csr"]),
    ("pp-shadow-dry-run", ["make", "-n", "-C", "tb/verilator/pp_shadow"]),
]
for key, argv in gates:
    result = subprocess.run([sys.executable, str(scratch / "run_gate.py"), key, *argv],
                            timeout=14500)
    if result.returncode:
        sys.exit(result.returncode)
