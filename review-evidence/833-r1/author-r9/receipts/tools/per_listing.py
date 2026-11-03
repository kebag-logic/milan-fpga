#!/usr/bin/env python3
"""Run owner_stated_seconds from a tree with every listing checked, not only up to the first that fails.

usage: python3 -I -B per_listing.py <tree>
Prints one line per listing: its words, then KEPT or MISSED (with the events). The starved cleanup of each
listing is the tree's own; only its result is compared here and then handed back as stated, so the control
goes on to its next listing. Exit 0 if every listing kept its seconds, 1 if any did not.
"""
import inspect
import sys
from pathlib import Path

tree = Path(sys.argv[1])
sys.path.insert(0, str(tree / "scripts"))
import test_suite_cancellation as tsc  # noqa: E402

real = tsc.starved_cleanup
results = []


def checked(owner, listing, names, stated, reaped=lambda _c: set()):
    words = inspect.currentframe().f_back.f_locals["words"]
    try:
        events = real(owner, listing, names, stated, reaped)
    except AssertionError as exc:
        events = f"AssertionError: {exc}"
    results.append((words, events == stated, events))
    return stated


tsc.starved_cleanup = checked
tsc.owner_stated_seconds()
for words, kept, events in results:
    print(f"{words}: {'KEPT' if kept else 'MISSED ' + str(events)[:200]}")
missed = [words for words, kept, _events in results if not kept]
print(f"per listing: {len(results)} listings, missed {missed}")
sys.exit(1 if missed else 0)
