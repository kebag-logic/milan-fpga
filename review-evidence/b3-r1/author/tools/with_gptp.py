#!/usr/bin/env python3
"""Run one bounded child command while a slave-only gPTP daemon disciplines
the controller NIC clock (controller host, under sudo).

usage: with_gptp.py <iface> <ptp4l> <cfg> <log> <settle_s> <limit_s> -- <child argv...>

ptp4l runs with -s (slave only: it never becomes grandmaster and never sends
Sync or Announce). The child starts once ptp4l reports servo state s2 with
|offset| < 1 us for 5 consecutive lines, or after <settle_s> with a note.
ptp4l is stopped (SIGTERM, then SIGKILL) when the child exits or <limit_s>
elapses. Nothing is detached. Exit code is the child's (124 on limit).
"""
import os
import re
import signal
import subprocess
import sys
import time


def main():
    sep = sys.argv.index("--")
    iface, ptp4l, cfg, log, settle, limit = sys.argv[1:sep]
    child = sys.argv[sep + 1:]
    settle, limit = float(settle), float(limit)
    t_end = time.monotonic() + limit
    signal.signal(signal.SIGTERM, lambda *a: (_ for _ in ()).throw(KeyboardInterrupt()))
    out = open(log, "w", buffering=1)
    ptp = subprocess.Popen([ptp4l, "-f", cfg, "-i", iface, "-s", "-m"],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    os.set_blocking(ptp.stdout.fileno(), False)
    good = 0
    buf = ""

    def pump():
        nonlocal good, buf
        try:
            chunk = ptp.stdout.read()
        except (BlockingIOError, TypeError):
            chunk = None
        if not chunk:
            return
        buf += chunk
        *lines, buf = buf.split("\n")
        for line in lines:
            out.write(f"{time.time():.3f} {line}\n")
            m = re.search(r"master offset\s+(-?\d+) s(\d)", line)
            if m:
                good = good + 1 if (m.group(2) == "2" and abs(int(m.group(1))) < 1000) else 0
            m = re.search(r"rms\s+(\d+)\s+max\s+(\d+)", line)
            if m:
                good = good + 1 if int(m.group(2)) < 1000 else 0

    rc = 124
    proc = None
    try:
        t0 = time.monotonic()
        while time.monotonic() - t0 < settle and good < 5 and ptp.poll() is None:
            pump()
            time.sleep(0.1)
        out.write(f"{time.time():.3f} WRAPPER settled={good >= 5} after {time.monotonic() - t0:.1f}s\n")
        if ptp.poll() is None:
            proc = subprocess.Popen(child)
            while proc.poll() is None and time.monotonic() < t_end:
                pump()
                time.sleep(0.1)
            if proc.poll() is None:
                proc.send_signal(signal.SIGINT)
                try:
                    proc.wait(5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
                rc = 124
            else:
                rc = proc.returncode
        else:
            rc = 3
    finally:
        if proc is not None and proc.poll() is None:
            proc.kill()
        ptp.send_signal(signal.SIGTERM)
        try:
            ptp.wait(5)
        except subprocess.TimeoutExpired:
            ptp.kill()
            ptp.wait()
        pump()
        out.write(f"{time.time():.3f} WRAPPER ptp4l rc={ptp.returncode} child rc={rc}\n")
        out.close()
    return rc


if __name__ == "__main__":
    sys.exit(main())
