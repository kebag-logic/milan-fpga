#!/usr/bin/env python3
"""Compare captured positive/negative includes and direct/shell compiler paths."""
import argparse
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument("checkout", type=Path)
ap.add_argument("scratch", type=Path)
a = ap.parse_args()
root = a.checkout.resolve()
work = a.scratch.resolve() / "boundary-probe"
work.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_capture as capture
import ctrl_boundary as boundary
import ctrl_configs as configs

copy = work / "root"
stack = copy / "third_party/tsn-c-stack"
firmware = copy / "sw/firmware/ctrl"
for tree in (stack / "include", stack / "src", firmware / "adp", firmware / "mbx"):
    tree.mkdir(parents=True, exist_ok=True)
(stack / "include/public.h").write_text("#define PUBLIC_VALUE 7\n")
(stack / "src/private.h").write_text("#define PRIVATE_VALUE 9\n")
(firmware / "mbx/platform.h").write_text("#define PLATFORM_VALUE 4\n")
good = firmware / "adp/good.c"
bad = firmware / "adp/bad.c"
reverse = stack / "src/bad.c"
good.write_text('#include "public.h"\nint good = PUBLIC_VALUE;\n')
bad.write_text('#include "private.h"\nint bad = PRIVATE_VALUE;\n')
reverse.write_text('#include "platform.h"\nint reverse = PLATFORM_VALUE;\n')
real = shutil.which("gcc")
inc = ["-I" + str(p) for p in (stack / "include", stack / "src", firmware / "mbx")]

def trial(name, source, call):
    where = work / name
    where.mkdir(exist_ok=True)
    obj = where / "probe.o"
    command = ["gcc", *inc, "-c", str(source), "-o", str(obj)]
    if call == "wrapped":
        invocation = "subprocess.run(" + repr(command) + ", check=True)"
    else:
        command[0] = real
        invocation = ("subprocess.run(" + repr(command) + ", check=True)" if call == "direct" else
                      "subprocess.run(" + repr(shlex.join(command)) + ", shell=True, check=True)")
    builder = where / "builder.py"
    builder.write_text("import subprocess\n" +
                      "subprocess.run(['gcc', '--version'], check=True, stdout=subprocess.DEVNULL)\n" +
                      invocation + "\n")
    recorded = where / "capture"
    result = capture.run(recorded, [sys.executable, str(builder)], cwd=where,
                         capture_output=True, text=True)
    c = capture.load(recorded)
    places = boundary.Places((copy, root), frozenset())
    findings = boundary.judged(c, places)
    errors = configs.unlisted(c) + configs.expanded(c, configs.places((copy, root)))
    row = {"case": name, "builder_rc": result.returncode, "object_created": obj.is_file(),
           "recorded_invocations": len(c.invocations),
           "recorded_sources": len([s for i in c.invocations for s in i.sources]),
           "bypasses": len(c.bypassed), "dependency_errors": len(errors),
           "boundary_findings": list(findings)}
    print(json.dumps(row), flush=True)
    assert result.returncode == 0 and obj.is_file()
    return row

rows = [trial("public-header", good, "wrapped"),
        trial("private-header", bad, "wrapped"),
        trial("stack-to-platform", reverse, "wrapped"),
        trial("absolute-direct-private", bad, "direct"),
        trial("absolute-shell-private", bad, "shell")]
assert not rows[0]["boundary_findings"]
assert rows[1]["boundary_findings"] and rows[2]["boundary_findings"]
assert rows[3]["bypasses"]
print("shell capture:", "ESCAPED" if not (rows[4]["boundary_findings"] or rows[4]["bypasses"] or
                                           rows[4]["dependency_errors"]) else "REFUSED")
