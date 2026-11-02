#!/usr/bin/env python3
"""At product constants, cancel a shell whose child exits on SIGTERM, so the shell is
resumed early in cleanup, and let its trap start a 6 s command. Report whether that
command was SIGKILLed at the 4 s point (grace + kill-all) or finished at about 6 s.

usage: early_resume_probe.py SCRIPTS_DIR
"""
import os, signal, sys, tempfile, threading, time
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import owned_process as op  # noqa: E402

sent = []
send = op.OwnedProcesses._send
signal_fn = op.OwnedProcesses._signal
marks = {}
OWNER = []


def noting_send(self, pid, start, signum):
    ok = send(self, pid, start, signum)
    if ok:
        sent.append((round(time.monotonic() - marks["cleanup"], 2), pid, signal.Signals(signum).name))
    return ok


def timed_signal(fd, signum):
    if (signum == signal.SIGCONT and "cleanup" in marks and "resume" not in marks
            and OWNER and fd == OWNER[0].root_fd):
        marks["resume"] = time.monotonic()
    return signal_fn(fd, signum)


cleanup = op.OwnedProcesses._cleanup


def timed_cleanup(self):
    marks.setdefault("cleanup", time.monotonic())
    return cleanup(self)


op.OwnedProcesses._send, op.OwnedProcesses._cleanup = noting_send, timed_cleanup
op.OwnedProcesses._signal = staticmethod(timed_signal)
with tempfile.TemporaryDirectory(prefix="r763-4-early-") as scratch:
    ready, done = Path(scratch) / "ready", Path(scratch) / "trap-command-done"
    script = (f"trap 'sleep 6 && echo done > \"{done}\"; exit 143' TERM\n"
              f"sleep 100 & touch \"{ready}\"\nwait\n")

    def cancel():
        while not ready.exists():
            time.sleep(0.02)
        time.sleep(0.2)
        os.kill(os.getpid(), signal.SIGTERM)
    threading.Thread(target=cancel, daemon=True).start()
    try:
        with op.OwnedProcesses() as owner:
            OWNER.append(owner)
            owner.run(["bash", "-c", script])
    except op.Cancelled:
        pass
    end = time.monotonic() - marks["cleanup"]
    resume = marks.get("resume", float("nan")) - marks["cleanup"]
    print(f"resume at {resume:.2f} s into cleanup; cleanup ended at {end:.2f} s")
    print(f"signals sent (s into cleanup, pid, signal): {sent}")
    print(f"trap command finished: {done.exists()}; SIGKILL sent at or before 4.5 s: "
          f"{any(s == 'SIGKILL' and t <= 4.5 for t, _p, s in sent)}")
