"""Exercise the public comparator through its CLI with planted populations.
Usage: python3 -B check_restore.py PACKET_DIRECTORY SCRATCH_DIRECTORY
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

packet, scratch = map(Path, sys.argv[1:])
scratch.mkdir(parents=True, exist_ok=True)
start = json.loads((packet / "restore-start.json").read_text())
end = json.loads((packet / "restore-end.json").read_text())

def row(doc, key):
    return next(r for r in doc["observations"] if r["observation"] == key)


def change_source(a, b):
    row(b, "census-clock-peer")["value"]["source"] ^= 1

def change_binding(a, b):
    row(b, "rx-state-peer-0")["value"]["connections"] = 1

def both_bound(a, b):
    for d in (a, b):
        row(d, "rx-state-peer-0")["value"]["connections"] = 1

def change_format(a, b):
    row(b, "format-peer-5-0")["value"]["format"] = "0205022001006000"

def missing_both(a, b):
    a["observations"].pop()
    b["observations"].pop()

def missing_one(a, b):
    b["observations"].pop()

def empty(a, b):
    a["observations"] = []
    b["observations"] = []

def failed(a, b):
    for d in (a, b):
        for r in d["observations"]:
            r["status"] = 1 if r["category"] == "bindings" else "NOT_IMPLEMENTED"

def duplicate(a, b):
    r = copy.deepcopy(b["observations"][0])
    r["value"]["connections"] = 1
    b["observations"][-1] = r

def wrong_descriptor(a, b):
    for d in (a, b):
        row(d, "format-peer-5-0")["descriptor_index"] = 1

def malformed(a, b):
    a["observations"][0] = None
    b["observations"][0] = None

def short_format(a, b):
    for d in (a, b):
        row(d, "format-peer-5-0")["value"]["format"] = "0205"

def short_map(a, b):
    for d in (a, b):
        row(d, "map-peer-0x000e-0-0")["value"]["mappings"].pop()

def conflicting_clock(a, b):
    for d in (a, b):
        row(d, "clock-dut")["value"]["source"] ^= 1

cases = [("equal_success", lambda a, b: None, 0)] + [(f.__name__, f, 1) for f in (change_source, change_binding, both_bound, change_format, missing_both, missing_one, empty, failed, duplicate, wrong_descriptor, malformed, short_format, short_map, conflicting_clock)]
results = []
for name, mutate, expected in cases:
    a, b = copy.deepcopy(start), copy.deepcopy(end)
    mutate(a, b)
    paths = [scratch / f"{name}-{tag}.json" for tag in ("start", "end")]
    for path, doc in zip(paths, (a, b)):
        path.write_text(json.dumps(doc))
    proc = subprocess.run(["timeout", "10s", sys.executable, "-B", str(packet / "restore_compare.py"), *map(str, paths)], capture_output=True, text=True, timeout=15)
    reply = json.loads(proc.stdout)
    ok = proc.returncode == expected and reply["pass_restore"] == (expected == 0) and not proc.stderr
    results.append(dict(case=name, expected_rc=expected, actual_rc=proc.returncode, passed=ok, result=reply))
print(json.dumps(dict(passed=all(r["passed"] for r in results), controls=len(results), cases=results), indent=2))
sys.exit(0 if all(r["passed"] for r in results) else 1)
