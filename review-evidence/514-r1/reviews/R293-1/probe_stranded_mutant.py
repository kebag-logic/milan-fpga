#!/usr/bin/env python3
"""Check whether the head self-test pins 'no retention line beside STRANDED'.

    python3 -B probe_stranded_mutant.py HEAD_SCRIPTS_DIR SCRATCH_DIR GIT_REPO
Mutant: the STRANDED branch of _report also prints a 'retained' retention line.
Runs (1) the mutant's full self-test and (2) head vs mutant on a stranded fixture.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

SRC, SCRATCH, REPO = (Path(a).resolve() for a in sys.argv[1:4])
work = SCRATCH / "retained-beside-stranded"
if work.exists():
    shutil.rmtree(work)
shutil.copytree(SRC, work)
path = work / "check_merge_containment.py"
before = b'            stranded += 1\n'
after = (b'            stranded += 1\n'
         b'            if current_retention:\n'
         b'                print(f"  retained   {label}: current retention: mutant")\n')
data = path.read_bytes()
assert data.count(before) == 1
path.write_bytes(data.replace(before, after))
p = subprocess.run([sys.executable, "-B", str(path), "--selftest"], cwd=REPO,
                   capture_output=True, text=True, errors="backslashreplace")
fails = sum(l.startswith("  FAIL") for l in p.stdout.splitlines())
print(f"mutant self-test: rc={p.returncode} PASS={'selftest: PASS' in p.stdout} FAIL-lines={fails}")
env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
           GIT_AUTHOR_NAME="F", GIT_AUTHOR_EMAIL="f@example.invalid",
           GIT_COMMITTER_NAME="F", GIT_COMMITTER_EMAIL="f@example.invalid",
           GIT_AUTHOR_DATE="@1790000000 +0000", GIT_COMMITTER_DATE="@1790000000 +0000")
repo = SCRATCH / "stranded-fixture"
if repo.exists():
    shutil.rmtree(repo)
repo.mkdir(parents=True)
for cmd in (["init", "-q", "-b", "main"], ["commit", "-q", "--allow-empty", "-m", "O"],
            ["checkout", "-qb", "pr"], ["commit", "-q", "--allow-empty", "-m", "unmerged"]):
    subprocess.run(["git", *cmd], cwd=repo, env=env, check=True)
(repo / "f").write_text("work\n")
subprocess.run(["git", "add", "f"], cwd=repo, env=env, check=True)
subprocess.run(["git", "commit", "-qm", "work"], cwd=repo, env=env, check=True)
for label, checker in (("head", SRC / "check_merge_containment.py"), ("mutant", path)):
    r = subprocess.run([sys.executable, "-B", "-I", str(checker), "--no-fetch", "--base", "main",
                        "pr", "--current-retention"], cwd=repo, env=env,
                       capture_output=True, text=True)
    lines = [l.strip() for l in r.stdout.splitlines() if l.strip()][:2]
    print(f"{label}: rc={r.returncode} {lines}")
