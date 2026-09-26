#!/usr/bin/env python3
"""Cancel the head runner while two unmarked sim_nxn legs run concurrently,
each with a live builder or image-generator descendant (#517 R245-4).

    probe_cancel_concurrent_nxn.py REPO WORKDIR SIGNAL
WORKDIR gets a mirror of the suite directory (symlinked entries, private
obj_legs/ and TMPDIR). The head's sim_pool.py runs
    --jobs=2 ./obj_nxn/Vmilan_dp_nxn ./obj_nxndv/Vmilan_dp_nxndv ./obj_nxn8/Vmilan_dp_nxn8
with stdout to a file. When both running legs have a python3 descendant, or
after both have started if their builder phases do not overlap, SIGNAL goes to
the runner. PASS requires: the runner ends by that signal; within 5 s no
process carries this probe's private TMPDIR marker in its environment; both
started legs are attributed as killed by the runner on SIGNAL; the third is
named as not started. Exit 0 on PASS, 1 on FAIL.
"""
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

REPO, WORK, SIG = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), signal.Signals[sys.argv[3]]
SUITE = REPO / "tb/verilator/milan_dp"
mirror = WORK / "tb/verilator/milan_dp"
mirror.mkdir(parents=True)
for entry in REPO.iterdir():
    if entry.name != "tb":
        (WORK / entry.name).symlink_to(entry)
for entry in SUITE.iterdir():
    if entry.name != "obj_legs":
        (mirror / entry.name).symlink_to(entry)
tmp = WORK / "tmp"
tmp.mkdir()
marker = f"R245_4_PROBE_{os.getpid()}"
env = dict(os.environ, TMPDIR=str(tmp), R245_PROBE_MARK=marker)
env.pop("MILAN_COUNTER_FRAME_OUT", None)


def tree() -> dict:
    """pid -> (ppid, argv, carries marker) for every process we can read."""
    rows = {}
    for pid in filter(str.isdigit, os.listdir("/proc")):
        try:
            stat = Path(f"/proc/{pid}/stat").read_bytes()
            argv = Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0")
            environ = Path(f"/proc/{pid}/environ").read_bytes()
        except OSError:
            continue
        fields = stat[stat.rfind(b")") + 2:].split()
        if fields[0] == b"Z":
            continue
        rows[int(pid)] = (int(fields[1]), [a.decode(errors="replace") for a in argv if a],
                          marker.encode() in environ)
    return rows


def descendants(rows: dict, root: int) -> list[int]:
    out, frontier = [], [root]
    while frontier:
        p = frontier.pop()
        kids = [c for c, (pp, _a, _m) in rows.items() if pp == p]
        out += kids
        frontier += kids
    return out


out = open(WORK / "runner.stdout", "wb")
runner = subprocess.Popen([sys.executable, "sim_pool.py", "--jobs=2", "./obj_nxn/Vmilan_dp_nxn",
                           "./obj_nxndv/Vmilan_dp_nxndv", "./obj_nxn8/Vmilan_dp_nxn8"],
                          cwd=mirror, env=env, stdin=subprocess.DEVNULL, stdout=out,
                          stderr=subprocess.STDOUT)
observed, t0 = None, time.monotonic()
while time.monotonic() - t0 < 20:
    rows = tree()
    legs = [p for p, (pp, argv, _m) in rows.items() if pp == runner.pid]
    helpers = {leg: [rows[d][1] for d in descendants(rows, leg)
                     if rows[d][1] and "python3" in rows[d][1][0]] for leg in legs}
    if len(legs) == 2 and all(helpers.values()):
        observed = {"mode": "both-legs-in-builder", "legs": {str(k): v for k, v in helpers.items()}}
        break
    if len(legs) == 2 and observed is None and any(helpers.values()) and time.monotonic() - t0 > 5:
        observed = {"mode": "one-leg-in-builder", "legs": {str(k): v for k, v in helpers.items()}}
        break
    time.sleep(0.005)
alive_before = [p for p, (_pp, _a, m) in tree().items() if m and p != runner.pid]
runner.send_signal(SIG)
code = runner.wait(timeout=30)
out.close()
survivors, t1 = [], time.monotonic()
while time.monotonic() - t1 < 5:
    survivors = [(p, a) for p, (_pp, a, m) in tree().items() if m]
    if not survivors:
        break
    time.sleep(0.05)
replay = (mirror / "obj_legs/replay.log").read_text(errors="replace")
checks = {
    "observed_live_descendants": observed is not None,
    "runner_ended_by_signal": code == -SIG,
    "no_survivor_with_marker": survivors == [],
    "nxn_attributed": f"./obj_nxn/Vmilan_dp_nxn was killed by this runner on {SIG.name}" in replay,
    "nxndv_attributed": f"./obj_nxndv/Vmilan_dp_nxndv was killed by this runner on {SIG.name}" in replay,
    "nxn8_named_unstarted": f"./obj_nxn8/Vmilan_dp_nxn8 was not started before {SIG.name}" in replay,
}
result = {"signal": SIG.name, "runner_exit": code, "observed": observed,
          "marked_processes_before_signal": len(alive_before), "survivors": survivors,
          "leftover_scratch_dirs": sorted(p.name for p in tmp.iterdir()),
          "checks": checks, "verdict": "PASS" if all(checks.values()) else "FAIL"}
(WORK / "result.json").write_text(json.dumps(result, indent=1) + "\n")
print(json.dumps(result))
sys.exit(0 if result["verdict"] == "PASS" else 1)
