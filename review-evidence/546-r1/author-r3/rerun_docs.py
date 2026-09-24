import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time

out = Path(sys.argv[1]).resolve()
root = Path.cwd()
# Activate the repository's pinned dependency environment before invocation.
env = dict(os.environ)
head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
rows = json.loads((out / "gate-results.json").read_text())
(out / "initial-gate-results.json").write_text(json.dumps(rows, indent=2) + "\n")
initial = out / "initial"
initial.mkdir(exist_ok=True)

def run(name, cwd=root):
    row = next(row for row in rows if row["name"] == name)
    shutil.copyfile(out / (name + ".log"), initial / (name + ".log"))
    start = time.monotonic()
    with (out / (name + ".log")).open("w") as log:
        result = subprocess.run(row["command"], cwd=cwd, env=env, stdout=log,
                                stderr=subprocess.STDOUT, timeout=1800)
    row.update(head=head, rc=result.returncode, seconds=round(time.monotonic() - start, 2))
    (out / "gate-results.json").write_text(json.dumps(rows, indent=2) + "\n")
    print(name, "rc", result.returncode, flush=True)
    print((out / (name + ".log")).read_text()[-1800:], flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)

run("docs-check")
with tempfile.TemporaryDirectory(prefix="546-a278-no-git-", dir="/tmp") as tmp:
    tree = Path(tmp) / "tree"
    tree.mkdir()
    archive = Path(tmp) / "source.tar"
    subprocess.run(["git", "archive", "--format=tar", "--output=" + str(archive), head], check=True, timeout=120)
    with tarfile.open(archive) as tar:
        tar.extractall(tree, filter="data")
    assert not (tree / ".git").exists()
    run("docs-check-no-git", tree)
for name in ["check_em_dash", "check_doc_style", "gen_toc", "check_doc_paths", "module_matrix", "git-diff-check", "committed-diff-check"]:
    run(name)
assert all(row["rc"] == 0 for row in rows)
print("ALL FINAL RESULTS RC 0", flush=True)
