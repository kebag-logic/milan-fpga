#!/usr/bin/env python3
"""R246-1: cancel the REAL ordinary pool while its stdout pipe is never read.

Usage: python3 real_cancel.py <suite-dir> <plan.json> <pool-line-index> <delay-s> <receipt.json>\n(a negative delay waits until an image-generator subprocess of a grouped leg is live)

Starts the recipe's own sim_pool line (from `make -n`) under /bin/sh in a new
session, stdout into a 4 KiB pipe nobody reads. After <delay-s>, pidfds are
taken on every live process in that session and every process whose command
line names the suite's executables or image generators, then SIGTERM goes to
the process group, as `timeout` does. Records: runner exit status and whether
it exited within 20 s, which snapshotted processes are still alive afterwards
(pidfds, so PID reuse cannot fake an answer), and the attribution lines in
obj_legs/replay.log. Only then is the pipe drained.
"""
import fcntl
import json
import os
import select
import signal
import subprocess
import sys
import time
from pathlib import Path


def snapshot(sid: int, suite: str) -> dict[int, str]:
    found = {}
    for entry in os.listdir("/proc"):
        if not entry.isdigit():
            continue
        pid = int(entry)
        try:
            cmd = Path(f"/proc/{pid}/cmdline").read_bytes().replace(b"\0", b" ").decode(errors="replace")
            stat = Path(f"/proc/{pid}/stat").read_bytes()
        except OSError:
            continue
        fields = stat[stat.rfind(b")") + 2:].split()
        if fields[0] == b"Z":
            continue
        psid = int(fields[3])
        cwd = ""
        try:
            cwd = os.readlink(f"/proc/{pid}/cwd")
        except OSError:
            pass
        if psid == sid or ("Vmilan_dp_" in cmd and cwd.startswith(suite)) or (
                ("endstation_builder" in cmd or "gen_aemi_image" in cmd) and cwd.startswith(suite)):
            found[pid] = cmd[:160]
    return found


def main() -> int:
    suite, plan, idx, delay, receipt = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), Path(sys.argv[5])
    line = json.load(open(plan))["lines"][idx]
    assert line.startswith("exec python3 sim_pool.py"), line
    rfd, wfd = os.pipe()
    fcntl.fcntl(wfd, fcntl.F_SETPIPE_SZ, 4096)
    err = open(receipt.with_suffix(".stderr"), "wb")
    runner = subprocess.Popen(["/bin/sh", "-c", line], cwd=suite, stdout=wfd, stderr=err,
                              start_new_session=True)
    os.close(wfd)
    if delay >= 0:
        time.sleep(delay)
        before = snapshot(runner.pid, suite)
    else:
        # negative delay: wait until a grouped leg's generator subprocess is live
        t_wait = time.monotonic()
        while True:
            before = snapshot(runner.pid, suite)
            if any("endstation_builder" in c or "gen_aemi_image" in c for c in before.values()):
                break
            assert time.monotonic() - t_wait < 300, "no generator subprocess observed"
            time.sleep(0.02)
    before.pop(os.getpid(), None)
    fds = {}
    for pid in before:
        try:
            fds[pid] = os.pidfd_open(pid)
        except OSError:
            pass
    t0 = time.monotonic()
    os.killpg(runner.pid, signal.SIGTERM)
    status = None
    while time.monotonic() - t0 < 20:
        status = runner.poll()
        if status is not None:
            break
        time.sleep(0.05)
    exit_s = time.monotonic() - t0
    # the runner's own pid is reaped by us; the rest must already be gone
    time.sleep(0.5)
    survivors = {}
    for pid, fd in fds.items():
        if pid == runner.pid:
            continue
        ev = select.poll()
        ev.register(fd, select.POLLIN | select.POLLHUP)
        r = ev.poll(0)
        if not (r and r[0][1] & select.POLLHUP):
            survivors[pid] = before[pid]
    after = snapshot(runner.pid, suite)
    queued_bytes = 0
    replay = Path(suite, "obj_legs/replay.log").read_text(errors="replace")
    os.set_blocking(rfd, False)
    drained = b""
    try:
        while True:
            chunk = os.read(rfd, 65536)
            if not chunk:
                break
            drained += chunk
    except BlockingIOError:
        pass
    result = dict(delay_s=delay, runner_status=status, runner_exit_within_s=round(exit_s, 3),
                  snapshot=before, survivors=survivors, live_after=after,
                  killed_lines=[l for l in replay.splitlines() if "killed by this runner" in l],
                  unstarted_lines=[l for l in replay.splitlines() if "was not started before" in l],
                  delivered_bytes=len(drained), transcript_bytes=len(replay.encode()),
                  delivered_is_prefix=replay.encode().startswith(drained))
    receipt.write_text(json.dumps(result, indent=1))
    print(json.dumps({k: v for k, v in result.items() if k != "snapshot"}, indent=1))
    ok = (status == -signal.SIGTERM and not survivors and not after and result["killed_lines"]
          and result["delivered_is_prefix"])
    print("REAL CANCELLATION:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
