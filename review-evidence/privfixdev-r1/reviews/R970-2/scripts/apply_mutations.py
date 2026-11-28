#!/usr/bin/env python3
"""Reviewer probe: plant one mutation in each of three disposable copies.

Usage: apply_mutations.py <scratch-dir>
<scratch-dir>/m1, m2 and m3 must each hold an untouched `git archive` copy of
scripts/, tb/tools/ and tests/ at the head under review.  Every mutation must
match exactly once, or the script stops.

M1  scripts/check_baremetal_only.py: the remote-root-shell rule no longer
    tolerates options between `ssh` and `root@`.  Target: the self-test arm
    whose fixture address this change rewrote.
M2  tb/tools/avtp_wire_truth_wire.py: the capture reader ignores the tap
    record header.  Target: the tap self-test and the retitled behave scenario.
M3  tb/tools/torture_campaign.py: a stream-scoped pcap wire source no longer
    convicts alone.  Target: the check whose fixture label this change rewrote.
"""
import pathlib
import sys

scratch = pathlib.Path(sys.argv[1])


def mutate(path: pathlib.Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise SystemExit(f"{path}: expected exactly one match, found {text.count(old)}")
    path.write_text(text.replace(old, new), encoding="utf-8")
    print("mutated", path.relative_to(scratch))


mutate(
    scratch / "m1/scripts/check_baremetal_only.py",
    r'r"(?<![A-Za-z0-9])ssh\s+(?:[^@\s]+\s+)*?root@"',
    r'r"(?<![A-Za-z0-9])ssh\s+root@"',
)
mutate(
    scratch / "m2/tb/tools/avtp_wire_truth_wire.py",
    "            data = data[tap_header:]\n",
    "            data = data[0:]\n",
)
mutate(
    scratch / "m3/tb/tools/torture_campaign.py",
    'or sides[l].get("source") == "pcap"}',
    'or sides[l].get("source") == "never"}',
)
