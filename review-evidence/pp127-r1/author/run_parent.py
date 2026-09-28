"""Replay the preserved parent harness against a committed donor head in scratch."""
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
out = Path(__file__).resolve().parent
source = out.parent / "606-a392"
scratch = Path("/tmp") / ("pp127-head-" + head[:12])
original = scratch / "original"
adapted = scratch / "expiry"
for target in (original, adapted):
    target.mkdir(parents=True, exist_ok=True)
    for name in ("reproduce.cpp", "run_reproduction.py"):
        shutil.copyfile(source / name, target / name)
shutil.copyfile("/tmp/pp127-parent-expiry/reproduce.cpp", adapted / "reproduce.cpp")
patch = difflib.unified_diff((original / "reproduce.cpp").read_text().splitlines(True),
                             (adapted / "reproduce.cpp").read_text().splitlines(True),
                             fromfile="parent/reproduce.cpp", tofile="scratch/reproduce.cpp")
(out / "parent-expiry-oracle.patch").write_text("".join(patch))

results = []
def run(name, command, expected):
    log = scratch / (name + ".log")
    with log.open("w") as stream:
        result = subprocess.run(command, cwd=repo, stdout=stream,
                                stderr=subprocess.STDOUT, timeout=1200)
    data = log.read_bytes()
    assert len(data) <= 200000
    (out / (name + ".log")).write_bytes(data)
    results.append(dict(name=name, command=command, rc=result.returncode,
                        expected_rc=expected, bytes=len(data),
                        sha256=hashlib.sha256(data).hexdigest()))
    print(f"{name}: rc={result.returncode}, expected={expected}", flush=True)
    if result.returncode != expected:
        print(data[-5000:].decode(errors="replace"), flush=True)
        raise RuntimeError("unexpected harness result")

# No Python 'deferred' argument: that would apply the old RTL counterfactual.
run("parent-original-oracle", ["python3", str(original / "run_reproduction.py"),
                               str(repo), str(original / "build")], 1)
# The C++ argument changes expectations and omits the helper that waits for LV.
run("parent-fixed-oracle", [str(original / "build/obj/reproduce"), "deferred"], 0)
run("parent-expiry-oracle", ["python3", str(adapted / "run_reproduction.py"),
                             str(repo), str(adapted / "build")], 0)

paths = [original / "reproduce.cpp", original / "run_reproduction.py",
         adapted / "reproduce.cpp", original / "build/obj/reproduce",
         adapted / "build/obj/reproduce", original / "build/build.log",
         adapted / "build/build.log"]
paths += [repo / "hdl/srp" / ("KL_srp_" + name + ".sv")
          for name in ("top", "encoder", "talker_fsm", "listener_fsm")]
manifest = []
for path in paths:
    data = path.read_bytes()
    manifest.append(dict(path=str(path), bytes=len(data),
                         sha256=hashlib.sha256(data).hexdigest()))
(out / "parent-results.json").write_text(json.dumps(
    dict(head=head, scratch=str(scratch), results=results, files=manifest), indent=2) + "\n")
print("Parent expiry-window replay and controls pass at " + head, flush=True)
