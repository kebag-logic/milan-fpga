#!/usr/bin/env python3
"""Build F5 twice through the recorder; judge an actual forbidden include."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument("root", type=Path)
p.add_argument("work", type=Path)
a = p.parse_args()
root, work = a.root.resolve(), a.work.resolve()
work.mkdir(parents=True, exist_ok=True)
clone = work / "checkout"
def git(*words, cwd=root):
    return subprocess.check_output(["git", *map(str, words)], cwd=cwd, text=True).strip()

head = git("rev-parse", "HEAD")
git("clone", "--quiet", "--shared", "--no-checkout", root, clone)
git("checkout", "--quiet", "--detach", head, cwd=clone)
for sub in ("third_party/tsn-c-stack", "gptp-processor", "protocol-processor",
            "third_party/lwSRP", "third_party/verilog-axis"):
    git("-c", "protocol.file.allow=always", "-c",
        "submodule." + sub + ".url=" + str(root / sub),
        "submodule", "update", "--init", sub, cwd=clone)
sys.path.insert(0, str(clone / "sw/firmware/ctrl/test"))
import ctrl_capture
import ctrl_boundary
from ctrl_configs import Scope, BUILDERS, held
from ctrl_build import Refusal

program = "tb/verilator/milan_dp/stream_counter_f5.py"
capture = work / "capture-clean"
for shape in ("1", "8"):
    result = ctrl_capture.run(capture, [sys.executable, program, "--build-only", "--shape", shape,
                             "--work", str(work / ("clean-" + shape))], cwd=clone,
                             capture_output=True, text=True)
    print(result.stdout, end="")
    assert result.returncode == 0, result.stderr
    assert "BUILT" in result.stdout and "F5_GAPS" not in result.stdout
    log = (work / ("clean-" + shape) / "run.log").read_text()
    print(log, end="")
    assert "built, not run (--build-only)" in log and "[PASS]" not in log
c = ctrl_capture.load(capture)
places = ctrl_boundary.Places((clone,), ctrl_boundary.targets(c, (clone,)))
found = ctrl_boundary.judged(c, places)
print("CAPTURE " + json.dumps({"invocations":len(c.invocations), "sources":sum(len(i.sources) for i in c.invocations),
                               "ran":sorted(c.ran), "findings":found}, default=list))
assert not found and program in c.ran and all(i.rc == 0 for i in c.invocations)
for inv in c.invocations:
    print("COMPILE " + json.dumps({"tool":inv.tool,"args":inv.args,"rc":inv.rc,
                                   "builders":sorted(inv.builders),"sources":[s.path for s in inv.sources]}))
scope = Scope(frozenset({"verilator"}))
# This isolated capture lacks unrelated builders. Compare only the named F5 refusal.
for label, known, cap in (("clean", BUILDERS, c),
                          ("removed-registry", tuple(b for b in BUILDERS if b.path != program), c),
                          ("removed-capture", BUILDERS, ctrl_capture.Capture((), (), (), ()))):
    try:
        held(cap, scope, known=known)
        text = ""
    except Refusal as exc:
        text = str(exc)
    f5 = [s.strip() for s in text.split(";") if program in s]
    print(label + " " + json.dumps(f5))
    assert bool(f5) == (label != "clean")

# Add a real, compilable include of the stack's private implementation to the firmware.
source = clone / "sw/firmware/ctrl/aecp/aecp_image.c"
original = source.read_bytes()
source.write_bytes(original + b'\n#include "../../../../third_party/tsn-c-stack/src/adp.c"\n')
try:
    bad = work / "capture-private"
    result = ctrl_capture.run(bad, [sys.executable, program, "--build-only", "--work", str(work / "private")],
                             cwd=clone, capture_output=True, text=True)
    print(result.stdout, end="")
    assert result.returncode == 0, result.stderr
    c = ctrl_capture.load(bad)
    places = ctrl_boundary.Places((clone,), ctrl_boundary.targets(c, (clone,)))
    found = ctrl_boundary.judged(c, places)
    print("PRIVATE INCLUDE " + json.dumps(found, default=list))
    assert any("aecp_image.c" in f and "src/adp.c" in f and "not one of" in f for f in found)
    assert any(program in builders for builders in found.values())
finally:
    source.write_bytes(original)
print("PASS: real F5 compiles recorded; clean passes, private source include refused; both removal controls named")
