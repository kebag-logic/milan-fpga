#!/usr/bin/env python3
"""usage: python3 -I probe_late_cancel_survivor.py <checkout> <cancel_after_s>

As probe_late_cancel.py (the endless listing at product constants, its command
already exited, cancellation arriving <cancel_after_s> into cleanup), then one
real descendant starts 1 s after the cancellation and outlives SIGKILL: the
owner's SIGKILL to it is dropped at its send, as the survivor control does,
since no unprivileged probe can build an unkillable process. Prints when the
run fails. The probe then really kills its survivor. Writes nothing."""
import os, signal, subprocess, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / "scripts"))
from owned_process import OwnedProcesses  # noqa: E402

cancel_after = float(sys.argv[2])
with OwnedProcesses() as owner:
    root = subprocess.Popen(["true"])
    owner.process = root
    owner.root_fd = os.pidfd_open(root.pid)
    root.wait()
    real_census, real_send = owner._descendants, owner._send
    gone = 2 ** 22 + 1
    since = time.monotonic()
    sent, survivor = [], []

    def listed() -> dict:
        elapsed = time.monotonic() - since
        if not sent and elapsed >= cancel_after:
            sent.append(elapsed)
            os.kill(os.getpid(), signal.SIGTERM)
        if sent and not survivor and elapsed >= sent[0] + 1.0:
            survivor.append(subprocess.Popen([sys.executable, "-c",
                                              "import signal,time\nsignal.signal(signal.SIGTERM, signal.SIG_IGN)\ntime.sleep(300)"]))
            survivor.append(elapsed)
        assert elapsed < 120, "no verdict in 120 s"
        return {gone: (os.getpid(), "0"), **real_census()}

    def undying(pid: int, start: str, signum: int) -> bool:
        if survivor and pid == survivor[0].pid and signum == signal.SIGKILL:
            return True
        return real_send(pid, start, signum)
    owner._descendants, owner._send = listed, undying
    owner._reap = lambda: {gone}
    try:
        owner._cleanup()
        print("NO FAILURE", flush=True)
    except RuntimeError as exc:
        print(f"verdict after {time.monotonic() - since:.2f} s wall; cancel sent at {sent}; "
              f"survivor started at {survivor[1] if survivor else None}; {str(exc)[:400]}", flush=True)
    if survivor:
        survivor[0].kill()
        survivor[0].wait()
    owner.cancel_signal = 0
    os.close(owner.root_fd)
    owner.root_fd = None
    owner.process = None
    owner._descendants, owner._send = (lambda: {}), real_send
