#!/usr/bin/env python3
"""Audit the resume-timing matrix of owner_stated_seconds: for each listing, the pass and clock of the
resume, the class of pass it falls in, and when a command the trap starts is first listed.

usage: python3 -I -B matrix_audit.py <tree>
A listing's census passes are its listing's calls, one per pass (the verdict's report reads it once more,
at the same clock, which is dropped).
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1])
sys.path.insert(0, str(tree / "scripts"))
import test_suite_cancellation as tsc  # noqa: E402

runs = []
real_cleanup = tsc.starved_cleanup


def cleanup(owner, listing, names, stated, reaped=lambda _c: set()):
    run = {"names": names, "passes": [], "words": None}
    runs.append(run)

    def listed(clock):
        entries = listing(clock)
        if not run["passes"] or run["passes"][-1][0] != clock:
            run["passes"].append((clock, sorted(names.get(pid, pid) for pid in entries)))
        return entries
    run["events"] = real_cleanup(owner, listed, names, stated, reaped)
    return run["events"]


real_kept_assert = None
tsc.starved_cleanup = cleanup
tsc.owner_stated_seconds()
GRACE, VERDICT = 2.0, 14.0
bad = 0
for n, run in enumerate(runs, 1):
    resumes = [e[0] for e in run["events"] if len(e) == 3 and e[1] == "SIGCONT"]
    clocks = [c for c, _ in run["passes"]]
    if not resumes:
        print(f"run {n}: no resume; {len(clocks)} passes; first listed: "
              + ", ".join(f"{name} from {next(c for c, l in run['passes'] if name in l):.7f}"
                          for name in sorted({x for _, l in run["passes"] for x in l})))
        continue
    r = resumes[0]
    i = clocks.index(r)
    before = clocks[i - 1] if i else None
    before2 = clocks[i - 2] if i > 1 else None
    after = clocks[i + 1] if i + 1 < len(clocks) else None
    if i == 0:
        klass = "first pass, inside grace"
    elif r < GRACE:
        klass = "a later pass inside grace" + (", the second" if i == 1 else "") + \
            (", the last before 2 s" if after is not None and after >= GRACE else "")
    elif before < GRACE:
        klass = "the first pass past grace"
    else:
        klass = "a later pass past grace" + (", the next after the first" if before2 is not None and before2 < GRACE
                                             else "") + (", the last before 14 s" if r + 0.5 >= VERDICT else "")
    alone_after = all(listed == ["shell"] for c, listed in run["passes"][i:] if c > r)
    command = [c for c, listed in run["passes"] if "trap command" in listed]
    trap = ("trap command first listed at %.7f, %s, %s" % (
        command[0], "the pass after the resume" if command[0] == after else
        "the resume pass" if command[0] == r else "pass %d" % clocks.index(command[0]),
        "inside grace (a SIGTERM pass)" if command[0] < GRACE else "past grace (a SIGKILL pass)")) if command else ""
    print(f"run {n}: resume at {r:.7f} in pass {i + 1}: {klass}; pass before {before}, after {after}; "
          f"{'shell alone after the resume' if alone_after else trap}")
print(f"matrix audit: {len(runs)} listings")
