#!/usr/bin/env python3
"""Drive the gate's real command line with baseline numbers written as long integer literals.

Usage: probe_bigint.py <repo checkout> <real route measurement directory> <scratch dir>
load() refuses NaN, Infinity and a decimal such as 1e400 that reads as infinity; this asks whether
the same magnitude written without a decimal point or exponent is refused too, or reaches judge().
"""
import json, subprocess, sys
from pathlib import Path

repo, real, scratch = (Path(arg).resolve() for arg in sys.argv[1:4])
gate = repo / "syn/ooc/pp_resource_gate.py"
scratch.mkdir(parents=True, exist_ok=True)
recorded = (repo / "syn/ooc/pp_resource_baseline.json").read_text()
BIG = "1" + "0" * 400

def run(label, text):
    path = scratch / "baseline.json"
    path.write_text(text)
    out = []
    for argv in (["check", str(real), "--endpoint", "route-1x1"], ["check-baseline"]):
        done = subprocess.run([sys.executable, "-B", str(gate), *argv, "--baseline", str(path)],
                              capture_output=True, text=True)
        trace = "Traceback" in done.stderr
        last = (done.stderr.strip().splitlines() or done.stdout.strip().splitlines() or [""])[-1]
        out.append(f"{argv[0]} rc {done.returncode}{' TRACEBACK' if trace else ''}: {last[:160]}")
    print(f"{label}\n    " + "\n    ".join(out))

def figure(name, value):
    data = json.loads(recorded)
    data["endpoints"]["route-1x1"]["record"]["figures"][name] = "@@"
    return json.dumps(data, indent=1).replace('"@@"', value)

run("control: the recorded baseline", recorded)
run("decimal 1e400 as the recorded WNS_ns (refused as designed)", figure("WNS_ns", "1e400"))
run("integer literal 10**400 as the recorded WNS_ns", figure("WNS_ns", BIG))
run("integer literal 10**400 as the recorded WHS_ns", figure("WHS_ns", BIG))
run("integer literal 10**400 as the recorded LUT (control: integer arithmetic)", figure("LUT", BIG))
