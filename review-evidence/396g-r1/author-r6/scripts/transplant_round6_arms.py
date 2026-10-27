#!/usr/bin/env python3
"""Run the round-6 self-test arms against the round-5 grader.

Usage: python3 -B transplant_round6_arms.py <old planner> <new planner> <work dir>

Copies the old planner, inserts the new planner's round-6 block (from the
`_FUZZ_SIZES` comment to the method before `test_audio_anchor_gaps_are_reported`)
at the same place, and defines `AUDIO_ARM_MISSED_REASON` as the reason the old
grader returns, so the arms run unmodified. Then runs each round-6 arm alone and
prints ok, FAIL or ERROR with the last line of its first problem.
"""
import subprocess
import sys
from pathlib import Path

ARMS = ("test_audio_compositions_never_pass_and_list_every_event",
        "test_audio_excursion_over_a_slip_arm_may_void",
        "test_audio_excursion_clearing_its_channel_number_is_split")
START = "    #: Issue #396 property fuzz:"
END = "    def test_audio_anchor_gaps_are_reported(self) -> None:"
OLD_REASON = 'AUDIO_ARM_MISSED_REASON = "void: a planted arm was missed"\n'
DRIVER = """
import sys, unittest
sys.path.insert(0, sys.argv[1])
import torture_campaign as t
class T(t._ReleaseGateChecks, unittest.TestCase):
    pass
result = unittest.TestResult()
T(sys.argv[2]).run(result)
problems = result.failures + result.errors
print("FAIL" if result.failures else "ERROR" if result.errors else "ok",
      problems[0][1].strip().splitlines()[-1][:200] if problems else "")
"""


def main() -> int:
    old, new, work = Path(sys.argv[1]).read_text(), Path(sys.argv[2]).read_text(), Path(sys.argv[3])
    block = new[new.index(START):new.index(END)]
    assert old.count(END) == 1 and START not in old
    anchor = "AUDIO_UNBALANCED_REASON = "
    line_end = old.index("\n", old.index(anchor)) + 1
    text = old[:line_end] + OLD_REASON + old[line_end:]
    text = text.replace(END, block + END)
    work.mkdir(parents=True, exist_ok=True)
    (work / "torture_campaign.py").write_text(text)
    for arm in ARMS:
        run = subprocess.run([sys.executable, "-B", "-I", "-c", DRIVER, str(work), arm],
                             capture_output=True, text=True, timeout=900)
        print(f"{arm}: {(run.stdout.strip() or run.stderr.strip()[-300:])}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
