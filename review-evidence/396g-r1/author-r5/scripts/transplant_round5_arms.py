#!/usr/bin/env python3
"""Run the round-5 audio arms against an older planner, unchanged otherwise.

Usage: python3 -I transplant_round5_arms.py <new torture_campaign.py> <old torture_campaign.py> <work dir>

Copies the old planner into <work dir>/tb/tools and replaces its region from
test_audio_constant_mask_beside_one_word_events up to
test_audio_anchor_gaps_are_reported with the new file's (the extended arm,
the unchanged code-bit arm, the sweep helpers and the four new arms). The old
planner lacks two names the new arms use, `_audio_net` and
`AUDIO_UNBALANCED_REASON`; the new file's definitions are added before
`self_test`, and nothing else changes. Each arm prints ok, FAIL or ERROR with
its first failing words. Exit status 0.
"""
import pathlib
import subprocess
import sys

new, old, work = (pathlib.Path(arg) for arg in sys.argv[1:4])
START = "    def test_audio_constant_mask_beside_one_word_events("
END = "    def test_audio_anchor_gaps_are_reported("
HOOK = "def self_test() -> int:\n"
new_text, old_text = new.read_text(encoding="utf-8"), old.read_text(encoding="utf-8")
for text in (new_text, old_text):
    assert text.count(START) == 1 and text.count(END) == 1 and text.count(HOOK) == 1
region = new_text[new_text.index(START):new_text.index(END)]
net = new_text[new_text.index("def _audio_net("):new_text.index("def _audio_upto(")]
reason = next(line for line in new_text.splitlines() if line.startswith("AUDIO_UNBALANCED_REASON = "))
grafted = old_text[:old_text.index(START)] + region + old_text[old_text.index(END):]
grafted = grafted.replace(HOOK, f"{reason}\n\n\n{net}{HOOK}")
target = work / "tb" / "tools"
target.mkdir(parents=True, exist_ok=True)
(target / "torture_campaign.py").write_text(grafted, encoding="utf-8")
ARMS = ("test_audio_constant_mask_beside_one_word_events", "test_audio_code_bit_corruption_ending_on_a_block",
        "test_audio_composition_sweep", "test_audio_slip_before_a_constant_mask",
        "test_audio_slip_totals_balance_the_bytes", "test_audio_arm_interplay_at_the_release_tolerance")
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
