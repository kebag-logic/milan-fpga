#!/usr/bin/env python3
"""Plant round-3 planner defects in a scratch copy of tests/ and tb/tools/ and
require the plan feature to fail on each.

Usage: python3 -I feature_mutants.py <scratch-root>

The scratch root holds tb/tools and tests exported from the exact head. Each
defect is a single-occurrence replacement in tb/tools/torture_campaign.py; the
pristine copy must pass first. Prints KILLED or SURVIVED with the first
failing scenario; exit 0 only when every defect is killed.
"""
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
src = root / "tb/tools/torture_campaign.py"
pristine = src.read_text()
MUTANTS = [
    ("qualified interval runs to the capture's end",
     "        return start, max(start, frames - AUDIO_GUARD_FRAMES)", "        return start, frames"),
    ("required duration not enforced", "    if end - start < required_s * layout.rate_hz:", "    if False:"),
    ("required duration defaults to a fraction of a second",
     "required_s: float = RELEASE_SOAK_DURATION_S) -> tuple[str, dict]:", "required_s: float = 0.1) -> tuple[str, dict]:"),
    ("capture-end stretch graded exactly",
     "    ending = track.reason == AUDIO_END_REASON and not track.acquiring", "    ending = False"),
    ("open words reported as a corruption",
     '    return {"capture_index": first, "class": "unresolved", "n": last - first + 1,',
     '    return {"capture_index": first, "class": "bit-flip", "n": last - first + 1,'),
    ("constant-mask track adopted as a slip",
     "        if mask:\n            slot.image = _AudioImage(", "        if False:\n            slot.image = _AudioImage("),
    ("held excursion never returns",
     "            if (found is not None and found[1] == image.tag and mask in (0, image.mask)",
     "            if (False and found is not None and found[1] == image.tag and mask in (0, image.mask)"),
    ("a run fits whole or not at all", "        if stop > j and (best is None or stop > best[1]):",
     "        if stop == end and (best is None or stop > best[1]):"),
    ("a loss at the event's own index not counted",
     "return index + sum(frames for at, frames in lost if at <= index)",
     "return index + sum(frames for at, frames in lost if at < index)"),
]


def behave() -> subprocess.CompletedProcess:
    return subprocess.run(["behave", "--no-capture", "-f", "plain", "features/torture_campaign_plan.feature"],
                          cwd=root / "tests", capture_output=True, text=True, timeout=600)


baseline = behave()
summary = [line for line in baseline.stdout.splitlines() if "scenarios passed" in line]
print(f"PRISTINE rc={baseline.returncode}: {summary[-1].strip() if summary else ''}")
rc = 1 if baseline.returncode else 0
for name, old, new in MUTANTS:
    if pristine.count(old) != 1:
        print(f"ANCHOR {name}: {pristine.count(old)}")
        rc = 1
        continue
    src.write_text(pristine.replace(old, new))
    run = behave()
    summary = [line for line in run.stdout.splitlines() if "scenarios passed" in line]
    fails = re.findall(r"Failing scenarios:\n((?:  .*\n)+)", run.stdout)
    first = fails[0].strip().splitlines()[0].strip() if fails else ""
    print(f"{'KILLED' if run.returncode else 'SURVIVED'}: {name}: "
          f"{summary[-1].strip() if summary else ''} | first: {first}")
    rc |= run.returncode == 0
src.write_text(pristine)
sys.exit(rc)
