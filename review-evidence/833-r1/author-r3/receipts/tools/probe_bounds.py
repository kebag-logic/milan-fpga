#!/usr/bin/env python3
"""Time a survivor's report under the shipped cleanup constants.

Usage: probe_bounds.py SCRIPTS_DIR LATE_SECONDS TRAP_SURVIVOR(0|1)

A stopped shell's background child ignores SIGTERM and its SIGKILL is dropped
delivered only LATE_SECONDS after the first signal (a slow death, as in state D). With
TRAP_SURVIVOR=1 the shell's TERM trap starts a second child whose SIGKILL is
always dropped (a true survivor). Prints the outcome and elapsed seconds.
Run inside a PID namespace.
"""
import os, signal, sys, tempfile, threading, time
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import owned_process
from owned_process import OwnedProcesses, Cancelled
from test_suite_cancellation import STUBBORN, published
late, trap_survivor = float(sys.argv[2]), sys.argv[3] == "1"
with tempfile.TemporaryDirectory(prefix="r763-bound-") as d:
    d = Path(d)
    r1, r2 = d / "r1", d / "r2"
    trap = f'"{sys.executable}" -c "$STUBBORN" "{r2}"; exit 143' if trap_survivor else "exit 143"
    script = f"trap '{trap}' TERM\n\"{sys.executable}\" -c \"$STUBBORN\" \"{r1}\" &\nwait\n"
    env = dict(os.environ, STUBBORN=STUBBORN)
    first = []; slow = []; second = []
    with OwnedProcesses() as owner:
        send = owner._send
        def hook(pid, start, signum):
            now = time.monotonic()
            if not first:
                first.append(now)
            if signum == signal.SIGKILL:
                if slow and pid == slow[0] and now < first[0] + late:
                    # Deliver it late through a pidfd, as a slow death would.
                    fd = os.pidfd_open(pid)
                    def deliver(fd=fd):
                        signal.pidfd_send_signal(fd, signal.SIGKILL)
                        os.close(fd)
                    threading.Timer(first[0] + late - now, deliver).start()
                    return True
                if r2.exists() and r2.read_text() and pid == int(r2.read_text()):
                    second.append(pid)
                    return True
            return send(pid, start, signum)
        owner._send = hook
        def cancel():
            slow.append(published(r1))
            os.kill(os.getpid(), signal.SIGTERM)
        threading.Thread(target=cancel, daemon=True).start()
        outcome = "returned"
        try:
            owner.run(["bash", "-c", script], env=env)
        except Cancelled:
            outcome = "cancelled, cleanup clean"
        except RuntimeError as exc:
            outcome = str(exc)
        elapsed = time.monotonic() - first[0]
        print(f"late={late} trap_survivor={trap_survivor} elapsed_from_first_signal={elapsed:.2f}s outcome: {outcome}", flush=True)
        owner.cancel_signal = 0
        if second:
            os.kill(second[0], signal.SIGKILL)
        os._exit(0)
