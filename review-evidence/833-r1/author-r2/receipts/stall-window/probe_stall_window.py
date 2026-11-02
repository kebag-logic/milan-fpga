#!/usr/bin/env python3
"""Run the shipped owner_stall control with the child's SIGKILL taking effect late.

Usage: probe_stall_window.py SCRIPTS_DIR DELAY_SECONDS
The owner's SIGKILL to the planted child is delivered DELAY_SECONDS later through
a pidfd, as a death slowed in state D would be. Prints PASS or FAIL with the
message. Run inside a PID namespace.
"""
import os, signal, sys, tempfile, threading, time
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import owned_process
import test_suite_cancellation as t
delay = float(sys.argv[2])
real_send = owned_process.OwnedProcesses._send
def slow_send(self, pid, start, signum):
    if signum == signal.SIGKILL and delay > 0:
        fd = os.pidfd_open(pid)
        def deliver(fd=fd):
            signal.pidfd_send_signal(fd, signal.SIGKILL)
            os.close(fd)
        threading.Timer(delay, deliver).start()
        return True
    return real_send(self, pid, start, signum)
owned_process.OwnedProcesses._send = slow_send
start = time.monotonic()
try:
    with tempfile.TemporaryDirectory(prefix="r763-stall-") as d:
        with owned_process.OwnedProcesses():
            t.owner_stall(Path(d))
except BaseException as exc:
    print(f"delay={delay} FAIL {time.monotonic() - start:.1f}s {type(exc).__name__}: {str(exc)[:300]}", flush=True)
    os._exit(1)
print(f"delay={delay} PASS {time.monotonic() - start:.1f}s", flush=True)
os._exit(0)
