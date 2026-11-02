#!/usr/bin/env python3
"""Show what each surviving reviewer mutant changes, on the head's own starved-clock harness.

usage: python3 -B probe_effect.py <scripts dir of the tree under test>
Three scenarios, production constants, owner_stated_seconds' starved clock (each pass
adds the 0.5 s cap, pass n at (n - 1) / 2 s):
  vanishing  a listing that dies inside every census (TESTING.md:232: 10 s more, under 44 s)
  parent     a placeholder parent whose live child outlives SIGKILL (TESTING.md:224: SIGKILL
             reaches every other descendant two seconds after grace, pass 9)
  by-number  a process that exits and is collected after _send's identity check
             (TESTING.md:219: signals go through the stable handle, never by number)
"""
import os
import signal
import subprocess
import sys

sys.path.insert(0, sys.argv[1])
import owned_process  # noqa: E402
import test_suite_cancellation as tsc  # noqa: E402
from owned_process import OwnedProcesses  # noqa: E402

gone, parent = 2 ** 22 + 1, 2 ** 22 + 2
child = os.getpid()
with OwnedProcesses() as owner, tsc.starved_clock():
    # vanishing: the owner's own reap collects the listed process in every pass.
    passes = []

    def census() -> dict:
        passes.append(True)
        assert len(passes) < 400
        return {gone: (os.getpid(), "1")}
    owner._descendants, owner._reap = census, lambda: {gone}
    try:
        owner._cleanup()
        verdict = "no verdict"
    except RuntimeError:
        verdict = "verdict"
    del owner._descendants, owner._reap
    print("vanishing:", verdict, "in pass", len(passes), "at", (len(passes) - 1) / 2, "s on the owner's clock")
    # parent: the child is this live process, listed under a placeholder parent.
    events = tsc.starved_cleanup(owner, lambda _n: {parent: (os.getpid(), "1"), child: (parent, "2")},
                                 {parent: "parent", child: "child"})
    print("parent:", [e for e in events if e[-1] in ("parent", "verdict") or e[1] == "verdict"])
# by-number: outside the starved clock; a real child exits after the identity check.
sleeper = subprocess.Popen(["sleep", "60"])
start = owned_process._identity(sleeper.pid)[1]
real_identity = owned_process._identity


def racing(pid: int):
    found = real_identity(pid)
    if pid == sleeper.pid:
        sleeper.kill()
        sleeper.wait()
    return found


owned_process._identity = racing
try:
    sent = OwnedProcesses()._send(sleeper.pid, start, signal.SIGTERM)
    print("by-number: _send returned", sent, "through the handle")
except ProcessLookupError as exc:
    print("by-number: _send signalled the number after its process was gone:", repr(exc))
finally:
    owned_process._identity = real_identity
