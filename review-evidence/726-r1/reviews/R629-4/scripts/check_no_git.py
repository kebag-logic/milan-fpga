#!/usr/bin/env python3
"""Run documentation checks from a disposable tracked-source export."""
import io
import pathlib
import subprocess
import sys
import tarfile

root, packet = map(pathlib.Path, sys.argv[1:])
destination = packet / "scratch/no-git-export"
destination.mkdir(exist_ok=True)
archive = subprocess.check_output(["git", "archive", "HEAD"], cwd=root)
with tarfile.open(fileobj=io.BytesIO(archive)) as contents:
    contents.extractall(destination, filter="data")
for script in ("docs_check.py", "check_feature_status.py"):
    subprocess.run([sys.executable, "scripts/" + script], cwd=destination, check=True)
