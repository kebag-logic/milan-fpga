#!/usr/bin/env python3
"""Reviewer probe: does a shell resumed at RESUME_AT s of cleanup (product constants) run its trap?

usage: trap_probe.py SCRIPTS_DIR RESUME_AT MARKER_DIR
A bash root with a TERM trap that writes a marker is cancelled while running, so it
is stopped and owned. One fake descendant stays live until RESUME_AT s into cleanup,
which holds the resume until then; afterwards it is gone. Prints whether the trap ran.
"""
import os, signal, sys, time
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import owned_process as op  # noqa: E402
resume_at, marker_dir = float(sys.argv[2]), Path(sys.argv[3])
marker_dir.mkdir(parents=True, exist_ok=True)
marker = marker_dir / "trap-ran"
FAKE = 2 ** 22 + 1
start, resumes, kills = [], [], []
with op.OwnedProcesses() as owner:
    real_desc, real_live, real_signal, real_send = owner._descendants, op._live, owner._signal, owner._send

    def t():
        return time.monotonic() - start[0] if start else 0.0

    def desc():
        if not start:
            start.append(time.monotonic())
        found = real_desc()
        if t() < resume_at:
            found[FAKE] = (os.getpid(), "0")
        return found

    def signalling(fd, signum):
        if fd == owner.root_fd and signum == signal.SIGCONT:
            resumes.append(round(t(), 2))
        real_signal(fd, signum)

    def send(pid, s, signum):
        if owner.process is not None and pid == owner.process.pid and signum == signal.SIGKILL:
            kills.append(round(t(), 2))
        return real_send(pid, s, signum)
    owner._descendants, owner._signal, owner._send = desc, signalling, send
    op._live = lambda pid: (t() < resume_at) if pid == FAKE else real_live(pid)
    signal.signal(signal.SIGALRM, lambda *_: os.kill(os.getpid(), signal.SIGTERM))
    signal.setitimer(signal.ITIMER_REAL, 0.5)
    outcome = "no exception"
    try:
        owner.run(["bash", "-c", f"trap 'echo ran > \"{marker}\"; exit 143' TERM; sleep 1000 & wait"])
    except op.Cancelled as exc:
        outcome = f"Cancelled {exc.signum}"
    except RuntimeError as exc:
        outcome = str(exc)[:200]
    owner.cancel_signal = 0
    op._live = real_live
print(f"RESULT resume_at={resume_at} resumes={resumes} shell_sigkill_at={kills} "
      f"trap_ran={marker.exists()} outcome={outcome}", flush=True)
