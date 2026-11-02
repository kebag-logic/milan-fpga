#!/usr/bin/env python3
"""usage: late_cancel_listing.py <scripts_dir> <cancel_at_seconds>

Falsification probe for the stated bound "a listing that dies inside every
census waits 10 s more: under 44 s". Production constants. A real command
(`true`) runs under OwnedProcesses.run and exits normally; its cleanup then
sees a listing that dies inside every census (the same substitution as the
owner_vanishing control). A cancellation signal arrives during that cleanup
at <cancel_at_seconds> of wall time, as an operator's SIGINT/SIGTERM can.
Prints the owner-clock time at which cleanup fails the run."""
import os, signal, sys, threading, time
sys.path.insert(0, sys.argv[1])
import owned_process
cancel_at = float(sys.argv[2])
gone = 2 ** 22 + 1
with owned_process.OwnedProcesses() as owner:
    real_census = owner._descendants
    state = {"cleanup": None}

    def listed():
        if state["cleanup"] is None:
            state["cleanup"] = time.monotonic()
            threading.Timer(cancel_at, os.kill, (os.getpid(), signal.SIGTERM)).start()
        assert time.monotonic() - state["cleanup"] < 120, "no verdict in 120 s"
        return {gone: (os.getpid(), "0")}
    owner._descendants = listed
    owner._reap = lambda: {gone}
    try:
        owner.run(["true"])
        print("RESULT: no failure", flush=True)
    except RuntimeError as exc:
        wall = time.monotonic() - state["cleanup"]
        print(f"RESULT: cancel at {cancel_at} s, root_notified={owner.root_notified}, "
              f"failed after {wall:.2f} s wall: {exc}", flush=True)
    except owned_process.Cancelled as exc:
        print(f"RESULT: Cancelled {exc}", flush=True)
    owner.cancel_signal = 0
