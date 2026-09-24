import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import time

out = Path(sys.argv[1]).resolve()
root = Path.cwd()
# Invoke from an environment containing the repository's pinned dependencies.
env = dict(os.environ, PYTHONUNBUFFERED="1")
head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
results = []

def run(name, command, cwd=root):
    print("START", name, flush=True)
    start = time.monotonic()
    with (out / (name + ".log")).open("w") as log:
        result = subprocess.run(command, cwd=cwd, env=env, stdout=log,
                                stderr=subprocess.STDOUT, timeout=7200)
    duration = round(time.monotonic() - start, 2)
    row = dict(name=name, command=command, head=head, rc=result.returncode, seconds=duration)
    results.append(row)
    (out / "gate-results.json").write_text(json.dumps(results, indent=2) + "\n")
    print("END", name, "rc", result.returncode, "seconds", duration, flush=True)
    body = (out / (name + ".log")).read_text(errors="replace")
    print("\n".join(body.splitlines()[-8:]), flush=True)
    return result.returncode

run("crf_rx", ["make", "-C", "tb/verilator/crf_rx"])
run("mmcm_servo", ["make", "-C", "tb/verilator/mmcm_servo"])
run("docs-check", ["python3", "scripts/docs_check.py"])
with tempfile.TemporaryDirectory(prefix="546-a278-no-git-", dir="/tmp") as tmp:
    tree = Path(tmp) / "tree"
    tree.mkdir()
    archive = Path(tmp) / "source.tar"
    subprocess.run(["git", "archive", "--format=tar", "--output=" + str(archive), head], check=True, timeout=120)
    with tarfile.open(archive) as tar:
        tar.extractall(tree, filter="data")
    assert not (tree / ".git").exists()
    run("docs-check-no-git", ["python3", "scripts/docs_check.py"], tree)
for name, command in [
    ("check_em_dash", ["python3", "scripts/check_em_dash.py", "--base", "57456af96b3127b9d309a995bbbd35a6113ce52d"]),
    ("check_doc_style", ["python3", "scripts/check_doc_style.py"]),
    ("gen_toc", ["python3", "scripts/gen_toc.py", "--check"]),
    ("check_doc_paths", ["python3", "scripts/check_doc_paths.py"]),
    ("module_matrix", ["python3", "docs/traceability/gen_module_matrix.py", "--check"]),
    ("xvlog_gate", ["python3", "scripts/xvlog_gate.py", "--check"]),
    ("check_cpp_idiom", ["python3", "scripts/check_cpp_idiom.py"]),
    ("check_py_idiom", ["python3", "scripts/check_py_idiom.py"]),
    ("measure_test_evidence", ["python3", "scripts/measure_test_evidence.py"]),
    ("measure_test_evidence-check", ["python3", "scripts/measure_test_evidence.py", "--check"]),
    ("git-diff-check", ["git", "diff", "--check"]),
    ("committed-diff-check", ["git", "diff", "--check", "d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1", "HEAD"]),
]:
    run(name, command)
print("ALL GATES FINISHED", flush=True)
raise SystemExit(1 if any(row["rc"] for row in results) else 0)
