#!/usr/bin/env python3
"""Run one command and observe its process tree from /proc (issue #517 benchmark).

    observe.py --log FILE --samples FILE --summary FILE [--interval S] -- CMD...

The command's stdout and stderr go to FILE exactly as scripts/run_all_suites.sh
sends a suite's make output to <suite>.log (one open file, `> log 2>&1`), so
the children see the same kind of descriptor they see in CI. Every INTERVAL
seconds (default 0.5) every descendant of the command is sampled: argv, cwd,
state, VmRSS, VmHWM, utime+stime, and the target of fd 0; plus the host's
1-minute load average and CPU busy fraction since the previous sample. For the
simulation legs the environment is hashed once, so two runs can be compared
for identical inputs.

This is benchmark instrumentation kept outside the repository: nothing in the
suite reads it, and none of its numbers is a test result.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

CLK_TCK = os.sysconf("SC_CLK_TCK")


def read(path: str) -> bytes | None:
    try:
        with open(path, "rb") as fh:
            return fh.read()
    except OSError:
        return None


def ppid_map() -> dict[int, int]:
    out = {}
    for entry in os.listdir("/proc"):
        if not entry.isdigit():
            continue
        raw = read(f"/proc/{entry}/stat")
        if raw is None:
            continue
        tail = raw[raw.rfind(b")") + 2:].split()
        out[int(entry)] = int(tail[1])
    return out


def descendants(root: int, parents: dict[int, int]) -> list[int]:
    children: dict[int, list[int]] = {}
    for pid, ppid in parents.items():
        children.setdefault(ppid, []).append(pid)
    found, stack = [], [root]
    while stack:
        pid = stack.pop()
        for child in children.get(pid, []):
            found.append(child)
            stack.append(child)
    return found


def cpu_busy() -> tuple[int, int]:
    raw = read("/proc/stat") or b""
    fields = [int(x) for x in raw.split(b"\n", 1)[0].split()[1:]]
    idle = fields[3] + fields[4]
    return sum(fields), idle


def describe(pid: int, env_seen: dict[int, str]) -> dict | None:
    stat = read(f"/proc/{pid}/stat")
    status = read(f"/proc/{pid}/status")
    cmdline = read(f"/proc/{pid}/cmdline")
    if stat is None or status is None or cmdline is None:
        return None
    tail = stat[stat.rfind(b")") + 2:].split()
    fields = {}
    for line in status.decode(errors="replace").splitlines():
        key, _, value = line.partition(":")
        fields[key] = value.strip()
    argv = [a.decode(errors="replace") for a in cmdline.split(b"\0") if a]
    try:
        cwd = os.readlink(f"/proc/{pid}/cwd")
    except OSError:
        cwd = None
    try:
        fd0 = os.readlink(f"/proc/{pid}/fd/0")
    except OSError:
        fd0 = None
    rec = {
        "pid": pid, "ppid": int(tail[1]), "state": tail[0].decode(),
        "argv": argv, "cwd": cwd, "fd0": fd0,
        "rss_kb": int(fields.get("VmRSS", "0 kB").split()[0] or 0),
        "hwm_kb": int(fields.get("VmHWM", "0 kB").split()[0] or 0),
        "cpu_s": (int(tail[11]) + int(tail[12])) / CLK_TCK,
    }
    if pid not in env_seen and argv and "Vmilan_dp_" in argv[0]:
        environ = read(f"/proc/{pid}/environ")
        if environ is not None:
            keys = sorted(k.split(b"=", 1)[0].decode(errors="replace")
                          for k in environ.split(b"\0") if k)
            env_seen[pid] = hashlib.sha256(environ).hexdigest()
            rec["env_sha256"] = env_seen[pid]
            rec["env_keys"] = keys
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", required=True)
    ap.add_argument("--samples", required=True)
    ap.add_argument("--summary", required=True)
    ap.add_argument("--interval", type=float, default=0.5)
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    args = ap.parse_args()
    cmd = args.cmd[1:] if args.cmd[:1] == ["--"] else args.cmd
    env_seen: dict[int, str] = {}
    with open(args.log, "wb") as log, open(args.samples, "w") as samples:
        t0 = time.monotonic()
        wall0 = time.time()
        proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT)
        last_total, last_idle = cpu_busy()
        status = None
        usage = None
        while status is None:
            now = time.monotonic() - t0
            total, idle = cpu_busy()
            busy = None
            if total > last_total:
                busy = round(1 - (idle - last_idle) / (total - last_total), 3)
            last_total, last_idle = total, idle
            procs = [r for r in (describe(p, env_seen)
                                 for p in descendants(proc.pid, ppid_map())) if r]
            load = (read("/proc/loadavg") or b"0").split()[0].decode()
            samples.write(json.dumps({"t": round(now, 3), "load1": float(load),
                                      "host_busy": busy, "procs": procs}) + "\n")
            samples.flush()
            try:
                pid, raw, usage = os.wait4(proc.pid, os.WNOHANG)
            except ChildProcessError:
                break
            if pid == proc.pid:
                status = raw
                break
            time.sleep(args.interval)
        wall = time.monotonic() - t0
    code = os.waitstatus_to_exitcode(status) if status is not None else None
    summary = {"cmd": cmd, "cwd": os.getcwd(), "started_utc": wall0,
               "wall_s": round(wall, 3), "exit": code,
               "children_user_s": round(usage.ru_utime, 3) if usage else None,
               "children_sys_s": round(usage.ru_stime, 3) if usage else None,
               "max_single_rss_kb": usage.ru_maxrss if usage else None}
    Path(args.summary).write_text(json.dumps(summary, indent=1) + "\n")
    print(json.dumps(summary))
    return 0 if code == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
