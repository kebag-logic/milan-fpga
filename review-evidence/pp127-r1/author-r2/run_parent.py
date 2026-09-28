"""Replay the archived parent sources against a supplied committed processor tree.

Usage: python3 run_parent.py PROCESSOR_TREE SCRATCH_DIRECTORY
All compilation and the original runner's generated results stay in scratch.
The original LV-anchored helper is a retained-semantics control. The manager's
accepted proof is the archived deadline-anchored patch, applied only to C++.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
scratch = Path(sys.argv[2]).resolve()
out = Path(__file__).resolve().parent
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
original = scratch / "original"
adapted = scratch / "deadline"
for target in (original, adapted):
    target.mkdir(parents=True, exist_ok=True)
    for name in ("reproduce.cpp", "run_reproduction.py"):
        shutil.copyfile(out / name, target / name)
subprocess.run(["patch", "--batch", "--fuzz=0", "-p1", "-i",
                str(out / "parent-expiry-oracle.patch")], cwd=adapted, check=True)
results = []


def run(name: str, command: list[str], expected: int) -> None:
    """Capture an exact foreground invocation and enforce its expected status."""
    log = scratch / (name + ".log")
    with log.open("w") as stream:
        result = subprocess.run(command, cwd=repo, stdout=stream,
                                stderr=subprocess.STDOUT, timeout=3600, check=False)
    data = log.read_bytes()
    record = dict(name=name, command=command, rc=result.returncode,
                  expected_rc=expected, bytes=len(data),
                  sha256=hashlib.sha256(data).hexdigest())
    results.append(record)
    if len(data) <= 200000:
        (out / log.name).write_bytes(data)
    print(f"{name}: rc={result.returncode}, expected={expected}", flush=True)
    if result.returncode != expected:
        print(data[-5000:].decode(errors="replace"), flush=True)
        raise RuntimeError("unexpected harness result")


# The Python runner never receives 'deferred': that would rewrite RTL.
run("parent-original-oracle", ["python3", str(original / "run_reproduction.py"),
                              str(repo), str(original / "build")], 1)
# Only the C++ executable receives the argument, selecting phase expectations.
run("parent-fixed-oracle", [str(original / "build/obj/reproduce"), "deferred"], 0)
run("parent-deadline-oracle", ["python3", str(adapted / "run_reproduction.py"),
                              str(repo), str(adapted / "build")], 0)
manifest = []
paths = [out / "reproduce.cpp", out / "run_reproduction.py",
         out / "parent-expiry-oracle.patch", adapted / "reproduce.cpp",
         original / "build/obj/reproduce", adapted / "build/obj/reproduce",
         original / "build/build.log", adapted / "build/build.log"]
for path in paths:
    data = path.read_bytes()
    manifest.append(dict(path=str(path), bytes=len(data),
                         sha256=hashlib.sha256(data).hexdigest()))
(out / "reproduce-deadline.cpp").write_bytes((adapted / "reproduce.cpp").read_bytes())
(out / "parent-results.json").write_text(json.dumps(
    dict(head=head, results=results, files=manifest), indent=2) + "\n")
print("Deadline-anchored parent proof and controls pass at " + head, flush=True)
