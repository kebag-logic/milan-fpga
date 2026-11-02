#!/usr/bin/env python3
"""A cancelled shell resumed inside grace: its trap's command keeps the shell's window.

Usage: python3 -I grace_resume_probe.py SCRIPTS_DIR [REPEATS]

Production stages (GRACE 2 s, KILL_ALL 2 s, TRAP 10 s, REAP 10 s). The shell's only
child exits on its SIGTERM in cleanup's first pass, so the shell is resumed while
the owner's clock is still inside grace. Its TERM trap then runs an external
command (sleep 1.0) and records it finished. docs/testing/TESTING.md's cleanup table
states: "From the resume the shell has ten seconds of its own to finish its terminal
trap, and so does any command that trap starts." Exit 0 when the trap's command
finished, 1 when it did not, each run's words on stdout.
"""
import os
import signal
import sys
import tempfile
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import owned_process  # noqa: E402
from owned_process import Cancelled, OwnedProcesses  # noqa: E402

CHILD = r'''
import os, sys, time
from pathlib import Path
Path(sys.argv[1]).write_text(str(os.getpid()))
while True:
    time.sleep(0.02)
'''


def once(scratch: Path) -> tuple[bool, str]:
    ready, marker, command = scratch / "ready", scratch / "trapped", scratch / "command-ran"
    script = (f"trap 'echo trapped > \"{marker}\"; sleep 1.0 && echo ran > \"{command}\"; exit 143' TERM\n"
              f"{sys.executable} -c \"$CHILD\" \"{ready}\" &\nwait\n")
    env = dict(os.environ, CHILD=CHILD)
    resumed_at, sent = [], []
    with OwnedProcesses() as owner:
        real_signal, real_send = owner._signal, owner._send
        began = []

        def signalling(fd: int, signum: int) -> None:
            if signum == signal.SIGCONT and owner.root_notified:
                resumed_at.append(time.monotonic())
            real_signal(fd, signum)

        def sending(pid: int, start: str, signum: int) -> bool:
            ok = real_send(pid, start, signum)
            if ok:
                if not began:
                    began.append(time.monotonic())
                sent.append((round(time.monotonic() - began[0], 2), pid, signal.Signals(signum).name))
            return ok
        owner._signal, owner._send = signalling, sending

        def cancel() -> None:
            deadline = time.monotonic() + 15
            while not (ready.exists() and ready.read_text()):
                assert time.monotonic() < deadline, "no handshake"
                time.sleep(0.01)
            os.kill(os.getpid(), signal.SIGTERM)
        threading.Thread(target=cancel, daemon=True).start()
        try:
            owner.run(["bash", "-c", script], env=env)
            return False, "cancellation was not reported"
        except RuntimeError as exc:
            owner.cancel_signal = 0
            return False, f"cleanup failed: {exc}"
        except Cancelled:
            # As the sweep's own controls do: the cancel is the expected result.
            owner.cancel_signal = 0
    resume = round(resumed_at[0] - began[0], 2) if resumed_at and began else None
    ok = marker.exists() and command.exists()
    words = ("trap command finished" if ok else
             "trap command did not finish inside the shell's window" if marker.exists() else
             "trap never ran")
    return ok, f"{words}; resume {resume} s after cleanup's first signal; signals {sent}"


def main() -> int:
    repeats = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    bad = 0
    for n in range(repeats):
        with tempfile.TemporaryDirectory(prefix="grace-resume-") as scratch:
            ok, words = once(Path(scratch))
        bad += not ok
        print(f"run {n + 1}: {'PASS' if ok else 'FAIL'}: {words}", flush=True)
    print(f"grace-resume: {'PASS' if not bad else 'FAIL'} ({repeats - bad} of {repeats} finished)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
