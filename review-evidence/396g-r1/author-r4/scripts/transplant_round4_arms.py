#!/usr/bin/env python3
"""Run the round-4 audio arms against an older planner, unchanged otherwise.

Usage: python3 -I transplant_round4_arms.py <new torture_campaign.py> <old torture_campaign.py> <work dir>

Copies the old planner into <work dir>/tb/tools, replaces its
test_audio_slip_and_corruption_share_a_window method with the new file's
region from `_corruption_first` up to test_audio_anchor_gaps_are_reported
(the changed arm and the four new arms), and runs those five arms. Each
arm prints ok, FAIL or ERROR with its first failing words. Exit status 0.
"""
import pathlib
import subprocess
import sys

new, old, work = (pathlib.Path(arg) for arg in sys.argv[1:4])
START_NEW = "    def _corruption_first("
START_OLD = "    def test_audio_slip_and_corruption_share_a_window("
END = "    def test_audio_anchor_gaps_are_reported("
new_text, old_text = new.read_text(encoding="utf-8"), old.read_text(encoding="utf-8")
for text, start in ((new_text, START_NEW), (old_text, START_OLD)):
    assert text.count(start) == 1 and text.count(END) == 1, start
region = new_text[new_text.index(START_NEW):new_text.index(END)]
grafted = old_text[:old_text.index(START_OLD)] + region + old_text[old_text.index(END):]
target = work / "tb" / "tools"
target.mkdir(parents=True, exist_ok=True)
(target / "torture_campaign.py").write_text(grafted, encoding="utf-8")
ARMS = ("test_audio_slip_and_corruption_share_a_window", "test_audio_block_slip_after_a_corruption_or_a_slip",
        "test_audio_planted_arms_beside_block_slips", "test_audio_constant_mask_beside_one_word_events",
        "test_audio_code_bit_corruption_ending_on_a_block")
DRIVER = """
import sys, unittest
sys.path.insert(0, sys.argv[1])
import torture_campaign as t
class T(t._ReleaseGateChecks, unittest.TestCase):
    pass
name = sys.argv[2]
result = unittest.TestResult()
T(name).run(result)
problems = result.failures + result.errors
print(name, "ok" if not problems else ("FAIL" if result.failures else "ERROR"),
      len(problems), "subtests" if problems else "")
for _, trace in problems[:2]:
    print("   ", trace.strip().splitlines()[-1][:300])
"""
for arm in ARMS:
    run = subprocess.run([sys.executable, "-B", "-I", "-c", DRIVER, str(target), arm],
                         capture_output=True, text=True, check=False)
    print(run.stdout.rstrip() or run.stderr.rstrip()[-400:], flush=True)
