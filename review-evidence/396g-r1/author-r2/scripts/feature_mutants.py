#!/usr/bin/env python3
"""Plant round-2 planner defects in a scratch copy of tests/ and tb/tools/ and
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
    ("counter repeats every 4096 samples",
     "block, offset = divmod(position % AUDIO_PERIOD_FRAMES, AUDIO_BLOCK_FRAMES)\n    bit =",
     "block, offset = divmod(position % 4096, AUDIO_BLOCK_FRAMES)\n    bit ="),
    ("block slips not located", "    if shift % AUDIO_BLOCK_FRAMES == 0:\n", "    if False:\n"),
    ("foreign channel number read as a swap", "return other if exchanged else None", "return other"),
    ("hold read as corruption",
     'if span[0][0] == "bad" or _audio_duplicate(track, labels, k):', 'if span[0][0] == "bad":'),
    ("identity changes not recorded", "                slot.timeline.append(found)\n", "                pass\n"),
    ("arms looked for on the logged channel only", "return found or [channel]", "return [channel]"),
    ("capture losses stop the clocks",
     "return index + sum(frames for at, frames in lost if at <= index)", "return index"),
    ("times extrapolated past the last anchor",
     '            timing = "unsupported: no anchor after the event"',
     '            wall, timing = here[1] + (index - here[0]) / layout.rate_hz, "anchored"'),
    ("arm edges widened to the halves", "edge = index // AUDIO_ARM_EDGE_DIVISOR", "edge = index // 2"),
    ("pending defaults accepted", "    if pending_at_default:\n", "    if False:\n"),
    ("cut outside its commit accepted", "if not window[0] <= cut.cut_s < window[1]:", "if False:"),
    ("missing cut evidence accepted",
     '        return "cut-phase evidence required: the commit window and the cut instant"', "        return None"),
    ("planted window need only meet the read interval",
     'if event["window_s"][0] <= interval[0] and interval[1] <= event["window_s"][1]]',
     'if event["window_s"][0] <= interval[1] and event["window_s"][1] >= interval[0]]'),
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
