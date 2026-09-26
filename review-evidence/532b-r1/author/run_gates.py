"""Run the assigned offline gates in the foreground and retain their exits."""
import json
import os
from pathlib import Path
import shlex
import subprocess
import tarfile
import tempfile
import time

out = Path(__file__).resolve().parent
repo = Path.cwd()
python_env = Path((out / "python-env.txt").read_text().strip())
env = dict(os.environ)
env["PATH"] = str(python_env / "bin") + os.pathsep + env["PATH"]
base = "7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a"
head = subprocess.run(["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
records = []

def gate(label, command, cwd=repo):
    print("START", label, shlex.join(command), flush=True)
    log = out / (label + ".log")
    started = time.monotonic()
    with log.open("w") as stream:
        result = subprocess.run(["rtk", "proxy", *command], cwd=cwd, env=env,
                                stdout=stream, stderr=subprocess.STDOUT, timeout=3600, check=False)
    record = {"gate": label, "command": shlex.join(command), "rc": result.returncode,
              "seconds": round(time.monotonic() - started, 2), "head": head, "log": log.name}
    records.append(record)
    (out / "gate-results.json").write_text(json.dumps(records, indent=2) + "\n")
    print("DONE", label, "rc=" + str(result.returncode), flush=True)
    lines = log.read_text(errors="replace").splitlines()
    print("\n".join(lines[-5:]), flush=True)

commands = [
    ("runner-isolated", ["python3", "-I", "scripts/act_ci.py", "--selftest"]),
    ("path-mutations", ["python3", "-B", str(out / "mutation_checks.py")]),
    ("slot-proof", ["bash", "scripts/act_slot_proof.sh", "--selftest"]),
    ("ci-events-check", ["python3", "scripts/ci_events.py", "--check"]),
    ("ci-events-selftest", ["python3", "scripts/ci_events.py", "--selftest"]),
    ("runner-contract", ["python3", "scripts/act_ci.py", "--selftest"]),
    ("docs-git", ["python3", "-B", "scripts/docs_check.py"]),
    ("em-dash", ["python3", "scripts/check_em_dash.py", "--base", base]),
    ("doc-style", ["python3", "scripts/check_doc_style.py"]),
    ("contents", ["python3", "scripts/gen_toc.py", "--check"]),
    ("python-idiom", ["python3", "scripts/check_py_idiom.py"]),
    ("shell-idiom", ["python3", "scripts/check_sh_idiom.py"]),
    ("diff-working", ["git", "diff", "--check"]),
    ("diff-base", ["git", "diff", "--check", base, "HEAD"]),
]
for label, command in commands:
    gate(label, command)
with tempfile.TemporaryDirectory(prefix="milan-532-no-git-") as raw:
    scratch = Path(raw)
    archive = scratch / "tree.tar"
    tree = scratch / "tree"
    tree.mkdir()
    subprocess.run(["rtk", "proxy", "git", "archive", "--format=tar", "--output", str(archive), head],
                   cwd=repo, check=True, timeout=300)
    with tarfile.open(archive) as bundle:
        bundle.extractall(tree, filter="data")
    assert not (tree / ".git").exists()
    gate("docs-no-git", ["python3", "-B", "scripts/docs_check.py"], cwd=tree)
raise SystemExit(0 if all(record["rc"] == 0 for record in records) else 1)
