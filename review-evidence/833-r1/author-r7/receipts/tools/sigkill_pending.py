#!/usr/bin/env python3
"""Does a SIGKILL to an unreaped child stay visible in its status ShdPnd/SigPnd, or as state Z, at every instant?"""
import os, signal, subprocess, sys, time
BLOCKING = r'''
import signal, time
signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGTERM, signal.SIGCONT})
print("ready", flush=True)
while True:
    time.sleep(0.02)
'''
def status(pid):
    s = dict(l.split(":", 1) for l in open(f"/proc/{pid}/status").read().splitlines())
    return int(s["SigPnd"], 16) | int(s["ShdPnd"], 16), s["State"].strip()
bad = 0
seen = {}
for i in range(int(sys.argv[1])):
    p = subprocess.Popen([sys.executable, "-c", BLOCKING], stdout=subprocess.PIPE, text=True)
    assert p.stdout.readline() == "ready\n"
    before = status(p.pid)
    os.kill(p.pid, signal.SIGKILL)
    samples = []
    t0 = time.monotonic()
    while time.monotonic() - t0 < 0.05:
        pend, state = status(p.pid)
        samples.append((bool(pend & (1 << 8)), state[0]))
    for s in set(samples):
        seen[s] = seen.get(s, 0) + 1
    if any(not k for k, _ in samples):
        bad += 1
    p.wait(); p.stdout.close()
print("before", before, "kinds", seen, "runs with a sample lacking the SIGKILL bit:", bad)
sys.exit(1 if bad else 0)
