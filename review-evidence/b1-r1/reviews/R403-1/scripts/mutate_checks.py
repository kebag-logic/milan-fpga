#!/usr/bin/env python3
"""Mutation probe over a DISPOSABLE copy of the archived packet.

For each planted defect in one action's analysis.json, run the author's
per-action verdict script (b1_check.py for cycles, b1_gmcheck.py for GM runs)
and this reviewer's rederive.py, and report which of them the defect kills.
The unmutated baseline must pass both and reproduce the archived check.txt
verdict line.

usage: mutate_checks.py <repo-checkout> <extracted-packet-dir>/author <scratch-dir>
"""
import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

repo, src, scratch = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
here = Path(__file__).resolve().parent
work = scratch / "mut" / "author"
if work.parent.exists():
    shutil.rmtree(work.parent)
shutil.copytree(src, work)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600,
                       env={"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin"})
    return r.returncode, r.stdout


def verdicts(action, checker):
    rc_a, out = run([sys.executable, "-B", str(work / "tools" / checker), action])
    rc_r, _ = run([sys.executable, "-B", str(here / "rederive.py"), str(repo), str(work)])
    return rc_a, (out.strip().splitlines() or [""])[-1], rc_r


def mutate(action, fn):
    p = work / "bench" / action / "analysis.json"
    orig = p.read_text()
    a = json.loads(orig)
    fn(a)
    p.write_text(json.dumps(a, indent=1) + "\n")
    return p, orig


def last_counter(a, key, idx, add):
    a["counter_endpoints"][key]["last"][idx] += add
    a["counter_endpoints"][key]["delta"][idx] += add
    for k, v in list(a["link_counters"].items()):
        if key == k and idx in ("0", "1"):
            v["end_LINK_UP" if idx == "0" else "end_LINK_DOWN"] += add


CASES = [
    ("cycle04", "b1_check.py", "baseline (no mutation)", lambda a: None),
    ("cycle04", "b1_check.py", "binding lost in one poll", lambda a: a["bindings"].update(all_connected=False, conn_counts=[0, 1])),
    ("cycle04", "b1_check.py", "DUT reset epoch 2 (a reboot)", lambda a: a.update(reset_epochs=[1, 2])),
    ("cycle04", "b1_check.py", "media servo ends in HOLDOVER", lambda a: a["servo"].append([99.0, dict(a["servo"][-1][1], state=5)])),
    ("cycle04", "b1_check.py", "gPTP never steady", lambda a: a.update(gptp_steady_from=None)),
    ("cycle04", "b1_check.py", "LINK_DOWN counted twice (+2)", lambda a: last_counter(a, "dut:counter-9-0", "1", 1)),
    ("cycle04", "b1_check.py", "LINK_UP not counted (+0)", lambda a: last_counter(a, "dut:counter-9-0", "0", -1)),
    ("cycle04", "b1_check.py", "MAC_STATUS never returns (no up edge)", lambda a: a.pop("mac_link_up")),
    ("gm03", "b1_gmcheck.py", "baseline (no mutation)", lambda a: None),
    ("gm03", "b1_gmcheck.py", "DUT listener unlocked once", lambda a: a["counter_endpoints"]["dut:counter-5-1"]["delta"].update({"1": 1})),
    ("gm03", "b1_gmcheck.py", "outgoing mr toggled at the takeover", lambda a: a["wire"]["dut"]["mr"].append([4.0, 0])),
    ("gm03", "b1_gmcheck.py", "talker MEDIA_RESET +1 at the takeover",
     lambda a: a["counter_transitions"]["dut:counter-6-1"].append([5.0, dict(a["counter_transitions"]["dut:counter-6-1"][-1][1], **{"2": a["counter_transitions"]["dut:counter-6-1"][-1][1]["2"] + 1})])),
    ("gm03", "b1_gmcheck.py", "servo left LOCKED mid-run then relocked",
     lambda a: a["servo"].insert(len(a["servo"]) // 2, [30.0, dict(a["servo"][0][1], state=5)])),
    ("gm03", "b1_gmcheck.py", "grandmaster not restored", lambda a: a["gm"].append([90.0, "0123456789abcdef"])),
]

rows = []
for action, checker, label, fn in CASES:
    p, orig = mutate(action, fn)
    rc_a, line, rc_r = verdicts(action, checker)
    p.write_text(orig)
    rows.append((action, label, rc_a, line, rc_r))
    print(f"{action:8s} {label:42s} author {checker} rc={rc_a} ({line}); reviewer rederive rc={rc_r}")

base_cycle = (src / "bench" / "cycle04" / "check.txt").read_text().strip().splitlines()[-1]
base_gm = (src / "bench" / "gm03" / "check.txt").read_text().strip().splitlines()[-1]
print(f"archived check.txt verdicts: cycle04={base_cycle} gm03={base_gm}")
shutil.rmtree(work.parent)
