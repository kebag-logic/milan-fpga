#!/usr/bin/env python3
"""Exercise real F5 and counter entry points against disposable bad stacks."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument("root", type=Path)
p.add_argument("work", type=Path)
a = p.parse_args()
root, work = a.root.resolve(), a.work.resolve()
work.mkdir(parents=True, exist_ok=True)
stack = work / "stack"

def run(cmd, cwd=root):
    result = subprocess.run([str(s) for s in cmd], cwd=cwd, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    return result.returncode, result.stdout

assert run(["git", "clone", "--quiet", "--no-hardlinks", root / "third_party/tsn-c-stack", stack])[0] == 0
pin = run(["git", "rev-parse", "HEAD:third_party/tsn-c-stack"])[1].strip()
assert run(["git", "-C", stack, "checkout", "--quiet", pin])[0] == 0
assert run([sys.executable, root / "sw/firmware/ctrl/test/ctrl_build.py", "--stack-pin", stack])[0] == 0
sentinel = work / "compiler-sentinel.sh"
marker = work / "compiler-reached"
sentinel.write_text('#!/bin/sh\nprintf "RECIPE REACHED\\n" >> "' + str(marker) + '"\nexit 91\n')
sentinel.chmod(0o755)
for state in ("modified", "off-pin"):
    assert run(["git", "-C", stack, "checkout", "--quiet", "--force", pin])[0] == 0
    if state == "modified":
        wire = stack / "include/wire.h"
        wire.write_bytes(wire.read_bytes() + b"\n#error R585_PIN_POISON\n")
        # The index must not be able to conceal the changed bytes.
        assert run(["git", "-C", stack, "update-index", "--assume-unchanged", "include/wire.h"])[0] == 0
        needle = "include/wire.h"
    else:
        assert run(["git", "-C", stack, "update-index", "--no-assume-unchanged", "include/wire.h"])[0] == 0
        assert run(["git", "-C", stack, "checkout", "--quiet", "--force", pin + "^"])[0] == 0
        needle = "is not the pinned"
    for shape in ("1", "8"):
        for build_only in (False, True):
            dest = work / f"{state}-f5-{shape}-{build_only}"
            cmd = [sys.executable, root / "tb/verilator/milan_dp/stream_counter_f5.py",
                   "--stack", stack, "--shape", shape, "--work", dest]
            if build_only:
                cmd += ["--build-only"]
            rc, out = run(cmd)
            print(json.dumps({"state":state,"shape":shape,"build_only":build_only,"rc":rc,"output":out.strip(),"staging_exists":dest.exists()}), flush=True)
            assert rc == 2 and "REFUSED:" in out and needle in out and not dest.exists()
    for target in ("counters", "counters-f5", "counters-mutants"):
        rc, out = run(["make", "-j16", "--no-print-directory", "-C", root / "tb/verilator/milan_dp",
                       "STACK_DIR=" + str(stack), "VERILATOR=" + str(sentinel), target])
        print(json.dumps({"state":state,"target":target,"rc":rc,"output":out.strip(),"compiler_reached":marker.exists()}), flush=True)
        assert rc != 0 and "REFUSED:" in out and needle in out and not marker.exists()
        assert "R585_PIN_POISON" not in out
print("PASS: clean pin accepted; 8 direct F5 and 6 make invocations refused before staging or compilation")
