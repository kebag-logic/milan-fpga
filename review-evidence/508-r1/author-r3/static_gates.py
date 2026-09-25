"""Run the assigned static gates sequentially, saving each command's exit code."""
from pathlib import Path
import subprocess
import sys

out = Path(__file__).resolve().parent
markdown = Path((out / "markdown-env.txt").read_text().strip()) / "bin/python"
gates = [
    ("docs-git", ["python3", "scripts/docs_check.py"]),
    ("docs-no-git", ["env", "GIT_DIR=/nonexistent-508-a297-git", "python3", "scripts/docs_check.py"]),
    ("em-dash", [str(markdown), "scripts/check_em_dash.py", "--base", "c266432dcb0cdd464205823a3d82cad260eedde2"]),
    ("doc-style", ["python3", "scripts/check_doc_style.py"]),
    ("toc", [str(markdown), "scripts/gen_toc.py", "--check"]),
    ("doc-paths", ["python3", "scripts/check_doc_paths.py"]),
    ("xvlog", ["python3", "scripts/xvlog_gate.py", "--check"]),
    ("cpp", ["python3", "scripts/check_cpp_idiom.py"]),
    ("python", ["python3", "scripts/check_py_idiom.py"]),
    ("port-contracts", ["python3", "scripts/check_port_contracts.py"]),
    ("naming", ["python3", "scripts/measure_naming.py", "--check"]),
    ("test-evidence", ["python3", "scripts/measure_test_evidence.py", "--check"]),
    ("whitespace", ["git", "diff", "--check"]),
    ("committed-whitespace", ["git", "diff", "--check", "c266432dcb0cdd464205823a3d82cad260eedde2", "HEAD"]),
    ("citations", ["python3", str(out / "prove_citations.py")]),
]
for name, command in gates:
    result = subprocess.run([sys.executable, str(out / "run_gate.py"), name, *command], check=False)
    if result.returncode:
        sys.exit(result.returncode)
