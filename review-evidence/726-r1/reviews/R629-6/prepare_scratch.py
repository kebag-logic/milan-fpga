#!/usr/bin/env python3
"""Prepare a disposable clone for the unit and retained-reset probe drivers."""
import argparse
import subprocess
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("root", type=Path)
a = p.parse_args()
root = a.root.resolve()
packet = Path(__file__).resolve().parent
scratch = packet / "scratch"
scratch.mkdir(exist_ok=True)
target = scratch / "suites"
head = "12f00129349c889e6dbbb7de11529ab38c9d164d"
assert subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip() == head
if not target.exists():
    subprocess.run(["git", "clone", "--shared", "--no-hardlinks", str(root), str(target)], check=True)
    subprocess.run(["git", "-C", str(target), "checkout", "--detach", head], check=True)
names = ("protocol-processor", "gptp-processor", "third_party/verilog-axis")
cmd = ["git", "-C", str(target), "-c", "protocol.file.allow=always"]
for name in names:
    cmd += ["-c", "submodule." + name + ".url=" + str(root / name)]
subprocess.run(cmd + ["submodule", "update", "--init", "--", *names], check=True)
assert subprocess.check_output(["git", "-C", str(target), "diff", "--name-only", head], text=True) == ""
print(target)
