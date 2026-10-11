#!/usr/bin/env python3
"""Run one partition of the control firmware's mutation campaigns, exactly as
test_ctrl_firmware.py --self-test calls them, so they can be spread over
concurrent processes.

usage: run_mutants.py <repo> <work-dir> <kind> <index> <count> <jobs>
kind: srp (full table, two interfaces), srpif1 (the IF=1 subset the gate
selects), ctrl (needs <work-dir>/../fwbuild/reuse from an arms run), aecp, pin.
Prints the campaign's own log and 'RESULT <kind> <index>/<count> PASS|FAIL'.
"""
import sys
from pathlib import Path

repo, work, kind, index, count, jobs = sys.argv[1:7]
index, count, jobs = int(index), int(count), int(jobs)
sys.path.insert(0, str(Path(repo) / "sw/firmware/ctrl/test"))
import ctrl_arms  # noqa: E402
import ctrl_mutants  # noqa: E402
import aecp_mutants  # noqa: E402
import srp_mutants  # noqa: E402
import srp_pub_mutants  # noqa: E402

lwsrp = (Path(repo) / "third_party/lwSRP").resolve()
root = Path(work) / f"{kind}-{index}-of-{count}"
full = srp_mutants.DEFECTS
if kind == "srp":
    srp_mutants.DEFECTS = full[index::count]
    print(f"srp partition: {len(srp_mutants.DEFECTS)} of {len(full)} defects")
    failed = srp_mutants.campaign(root, lwsrp, jobs)
elif kind == "srpif1":
    subset = tuple(d for d in full if d.name.startswith(("four-way-", "binding-", "feedback-", "r10-", "p11-",
                                                         "srp-bound-", "srp-term-", "srp-poll-extra",
                                                         "srp-send-extra", *srp_pub_mutants.ROUND5)))
    srp_mutants.DEFECTS = subset[index::count]
    print(f"srp IF=1 partition: {len(srp_mutants.DEFECTS)} of {len(subset)} defects")
    failed = srp_mutants.campaign(root, lwsrp, jobs, 1)
elif kind == "ctrl":
    reuse = (Path(work).parent / "fwbuild/reuse").resolve()
    failed = ctrl_mutants.campaign(root, reuse, jobs, (1, 1), [index, count])
elif kind == "aecp":
    failed = aecp_mutants.campaign(root, jobs, (index, count))
elif kind == "pin":
    root.mkdir(parents=True, exist_ok=True)
    failed = ctrl_mutants.lwsrp_pin_arms(root, lwsrp) != 0
else:
    sys.exit(f"unknown kind {kind}")
print(f"RESULT {kind} {index}/{count} {'FAIL' if failed else 'PASS'}")
sys.exit(1 if failed else 0)
