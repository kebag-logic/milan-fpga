#!/usr/bin/env python3
"""Drive the gate's real command line (a real stdout, not a captured buffer) with baselines whose
names hold a JSON-escaped lone surrogate, and with duplicate JSON keys.

Usage: probe_text.py <repo checkout> <real route measurement directory> <scratch dir>
Each case prints the exit status of check and check-baseline and whether a traceback escaped.
The gate's stated contract: 0 within tolerance, 1 a material regression only, 2 for every input it
cannot judge, never through a traceback.
"""
import json, subprocess, sys
from pathlib import Path

repo, real, scratch = (Path(arg).resolve() for arg in sys.argv[1:4])
gate = repo / "syn/ooc/pp_resource_gate.py"
scratch.mkdir(parents=True, exist_ok=True)
recorded = (repo / "syn/ooc/pp_resource_baseline.json").read_text()

def edit_obj(change):
    data = json.loads(recorded)
    change(data)
    return json.dumps(data, indent=1)  # ensure_ascii: a lone surrogate is written as the escape \ud800

def run(label, text):
    path = scratch / "baseline.json"
    path.write_text(text)
    results = []
    for argv in (["check", str(real), "--endpoint", "route-1x1"], ["check-baseline"]):
        done = subprocess.run([sys.executable, "-B", str(gate), *argv, "--baseline", str(path)],
                              capture_output=True, text=True, errors="backslashreplace")
        trace = "Traceback" in done.stderr
        last = (done.stderr.strip().splitlines() or done.stdout.strip().splitlines() or [""])[-1]
        results.append(f"{argv[0]} rc {done.returncode}{' TRACEBACK' if trace else ''}: {last[:150]}")
    print(f"{label}\n    " + "\n    ".join(results))

run("control: the recorded baseline", recorded)
run("A: an extra endpoint named with a lone surrogate (a copy of route-1x1)",
    edit_obj(lambda d: d["endpoints"].update({"\ud800": d["endpoints"]["route-1x1"]})))
run("B: an unknown endpoint field named with a lone surrogate",
    edit_obj(lambda d: d["endpoints"]["route-1x1"].update({"\ud800": 1})))
run("C: an unknown file field named with a lone surrogate",
    edit_obj(lambda d: d.update({"\ud800": 1})))
run("D: a route-1x1 sub-block scope named with a lone surrogate (valid counts)",
    edit_obj(lambda d: d["endpoints"]["route-1x1"]["record"]["scopes"].update(
        {"\ud800": dict(d["endpoints"]["route-1x1"]["record"]["scopes"]["wrapper"])})))
run("E: an extra endpoint named with an ordinary non-ASCII name (control for the surrogate)",
    edit_obj(lambda d: d["endpoints"].update({"réroute": d["endpoints"]["route-1x1"]})))
dup = recorded.replace('"tolerance": {', '"tolerance": {"LUT": 99999,', 1)
run("F: a duplicate tolerance key (first LUT 99999, last as recorded)", dup)
