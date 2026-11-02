#!/usr/bin/env python3
"""usage: withbuilds.py <clones> -- COMMAND ...  Scratch only. Runs COMMAND beside real build loops in that many clones, each in its own session,
all stopped by killing their process groups when it ends."""
import os, signal, subprocess, sys, time
n = int(sys.argv[1]); assert sys.argv[2] == "--"
S = "$VALIDATION_STORAGE/833-a726"
loads = [subprocess.Popen([f"{S}/load/buildloop.sh", f"{S}/full/after-{i}"], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) for i in range(n)]
time.sleep(25)
try:
    rc = subprocess.run(sys.argv[3:]).returncode
finally:
    for p in loads:
        os.killpg(p.pid, signal.SIGKILL)
    for p in loads:
        p.wait()
sys.exit(rc)
