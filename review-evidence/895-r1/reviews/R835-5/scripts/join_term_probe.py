#!/usr/bin/env python3
"""join_term_probe.py TREE OUT

Reviewer probe (not in the tree's campaign): plant SRP_REDECLARE_CS without its JoinTime term, keeping THE
TRANSMIT's, through the tree's own SRP campaign machinery (srp_mutants.campaign), once against the new
Talker.ChangedDestinationWaitsTwoLeaveAllTimePeriodsAfterTheLatestLeave and once against the earlier
Talker.ChangedDestinationWaitsTwoLeaveAllTimePeriods, at 8x8/2if and 1x1/1if. Read-only on TREE; each plant goes
into the campaign's disposable copy under OUT. Exit 1 when a plant escaped."""
import dataclasses
import sys
from pathlib import Path

tree, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(tree / 'sw/firmware/gtest'))
import srp_mutants  # noqa: E402
import srp_talker_mutants as t  # noqa: E402

base = next(d for d in srp_mutants.DEFECTS if d.name == 'talker-hold-off-drops-the-transmit-term')
new = t.REDECLARE.replace(' + SRP_JOIN_CS', '')
assert new != t.REDECLARE
srp_mutants.DEFECTS = (
    dataclasses.replace(base, name='probe-hold-off-drops-the-join-term-latest', new=new),
    dataclasses.replace(base, name='probe-hold-off-drops-the-join-term-earlier', test=t.CHANGED,
                        needle='the changed destination comes no sooner than two LeaveAllTime periods after the Leave'),
)
srp_mutants.DEFECTS = (srp_mutants.DEFECTS[0], dataclasses.replace(srp_mutants.DEFECTS[1], new=new))
lwsrp = (tree / 'third_party/lwSRP').resolve()
failed = False
for n in (2, 1):
    print(f"== interfaces {n}", flush=True)
    failed = srp_mutants.campaign(out / f"if{n}", lwsrp, 4, n) or failed
print(f"join-term probe: {'an escape' if failed else 'every plant caught'}")
sys.exit(1 if failed else 0)
