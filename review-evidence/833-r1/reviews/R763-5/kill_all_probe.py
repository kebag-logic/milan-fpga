#!/usr/bin/env python3
"""Pass-by-pass signals for a stubborn parent whose child outlives SIGKILL, on the starved clock.

Usage: python3 -I kill_all_probe.py <tree>
Uses the tree's own owner_stated_seconds helpers (starved_clock, starved_cleanup):
every pass adds 0.5 s of owner clock, so pass n is at (n - 1) / 2 s. TESTING.md:223-224
state SIGKILL to a stubborn leaf at 2 s (pass 5) and to every other descendant
two seconds later, 4 s (pass 9); a survivor fails the run at 14 s (pass 29).
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / "scripts"))
import test_suite_cancellation as t  # noqa: E402
from owned_process import OwnedProcesses  # noqa: E402

parent, owner_pid = 2 ** 22 + 5, 2 ** 22 + 4  # never real processes
child = os.getpid()           # always live: a child that outlives its SIGKILL
names = {parent: "parent", child: "child"}
with OwnedProcesses() as owner, t.starved_clock():
    events = t.starved_cleanup(owner, lambda _n: {parent: (owner_pid, "1"), child: (parent, "2")}, names)
for event in events:
    print(event)
kills = [n for n, *rest in events if rest == ["SIGKILL", "parent"]]
print("parent first SIGKILL in pass", kills[:1], "expected [9] (4 s)")
sys.exit(0 if kills[:1] == [9] else 1)
