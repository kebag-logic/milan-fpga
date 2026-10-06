#!/usr/bin/env python3
"""Rebuild only the shared mailbox checks in a disposable exact-head tree."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import tarfile
p = argparse.ArgumentParser()
p.add_argument("repo", type=Path)
p.add_argument("verilator", type=Path)
a = p.parse_args()
work = Path(__file__).resolve().parent / "scratch" / "mailbox"
work.mkdir(parents=True, exist_ok=True)
verilator = a.verilator.resolve()
identity = subprocess.check_output([str(verilator), "--version"], text=True).strip()
print(identity, flush=True)
assert "Verilator 5.050 " in identity
archive = work / "head.tar"
with archive.open("wb") as out:
    subprocess.run(["git", "archive", "HEAD"], cwd=a.repo, stdout=out, check=True)
tree = work / "tree"
tree.mkdir(exist_ok=True)
with tarfile.open(archive) as tar:
    tar.extractall(tree, filter="data")
wrapper = work / "verilator-limited"
wrapper.write_text("#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i,v in enumerate(a[:-1]):\n    if v == '-j': a[i+1]='4'\nos.execv(" + repr(str(verilator)) + ", [" + repr(str(verilator)) + "]+a)\n")
wrapper.chmod(0o755)
env = dict(os.environ, VERILATOR=str(wrapper))
where = tree / "tb/verilator/mbx"
for target in ("run-wb", "run-axil", "run-cosim"):
    print("RUN make -j16 " + target, flush=True)
    subprocess.run(["make", "-j16", target], cwd=where, env=env, check=True)
subprocess.run([sys.executable, "-B", "mutants.py", "--quick", "--jobs", "1", "--keep", str(work / "mutants")],
               cwd=where, env=env, check=True)
