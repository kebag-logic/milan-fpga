#!/usr/bin/env python3
"""usage: python3 -I probe_late_cancel.py <checkout> <cancel_after_s|none>

Times owned cleanup of the endless listing (one entry that dies inside every
census, as the vanishing control plants it) at the product constants, on an
idle-enough host where every pass stays well under 0.5 s, so the owner's clock
equals wall time. With <cancel_after_s>, a cancellation signal reaches the
owner that many seconds into cleanup, after its command already exited: the
case where the command finished and cancellation arrives during cleanup.
Prints the time to the CLEANUP FAILED verdict. Writes nothing."""
import os, signal, subprocess, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / "scripts"))
import owned_process  # noqa: E402
from owned_process import OwnedProcesses  # noqa: E402

cancel_after = None if sys.argv[2] == "none" else float(sys.argv[2])
print("constants", dict(GRACE=owned_process.GRACE_SECONDS, KILL_ALL=owned_process.KILL_ALL_SECONDS,
                        TRAP=owned_process.TRAP_SECONDS, REAP=owned_process.REAP_SECONDS,
                        MAX_PASS=owned_process.MAX_PASS_SECONDS), flush=True)
with OwnedProcesses() as owner:
    # The command has exited and been collected; its handle stays open, as in run().
    root = subprocess.Popen(["true"])
    owner.process = root
    owner.root_fd = os.pidfd_open(root.pid)
    root.wait()
    gone = 2 ** 22 + 1
    since = time.monotonic()
    sent = []

    def listed() -> dict:
        if cancel_after is not None and not sent and time.monotonic() - since >= cancel_after:
            sent.append(time.monotonic() - since)
            os.kill(os.getpid(), signal.SIGTERM)
        assert time.monotonic() - since < 120, "no verdict in 120 s"
        return {gone: (os.getpid(), "0")}
    owner._descendants = listed
    owner._reap = lambda: {gone}
    try:
        owner._cleanup()
        print("NO FAILURE", flush=True)
    except RuntimeError as exc:
        print(f"verdict after {time.monotonic() - since:.2f} s wall; cancel sent at {sent}; "
              f"root_notified={owner.root_notified}; {str(exc)[:160]}", flush=True)
    owner.cancel_signal = 0
    os.close(owner.root_fd)
    owner.root_fd = None
    owner.process = None
    owner._descendants = lambda: {}
