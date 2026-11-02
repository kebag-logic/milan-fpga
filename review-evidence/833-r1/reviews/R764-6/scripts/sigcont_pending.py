#!/usr/bin/env python3
"""Feasibility probe: a blocked SIGCONT sent by number stays pending in /proc status (review probe)."""
import os, signal, subprocess, sys, time
child = subprocess.Popen([sys.executable, "-c", "import signal,time\n"
                          "signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGTERM, signal.SIGCONT})\n"
                          "print('ready', flush=True)\nwhile True: time.sleep(0.02)"], stdout=subprocess.PIPE, text=True)
assert child.stdout.readline() == "ready\n"
def pending():
    s = dict(l.split(":", 1) for l in open(f"/proc/{child.pid}/status").read().splitlines())
    return int(s["SigPnd"], 16) | int(s["ShdPnd"], 16)
before = pending() & (1 << (signal.SIGCONT - 1))
os.kill(child.pid, signal.SIGCONT)
after = pending() & (1 << (signal.SIGCONT - 1))
child.kill(); child.wait()
print(f"SIGCONT pending before={bool(before)} after-send={bool(after)}")
sys.exit(0 if (not before and after) else 1)
