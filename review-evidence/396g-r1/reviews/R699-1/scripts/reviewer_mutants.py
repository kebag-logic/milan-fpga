#!/usr/bin/env python3
"""Reviewer-owned mutants for the #396 release planner, oracles and grader.

Usage: python3 -I reviewer_mutants.py <pristine export root> <work dir> [jobs]

The export root holds tb/tools and tests from the exact head (git archive).
Each mutant copies it, applies one exact single-occurrence replacement to
tb/tools/torture_campaign.py, then runs the planner self-test and the plan
feature from the copy. KILLED means at least one of the two returned
nonzero. Prints one line per mutant and a summary; exit 0.
"""
import concurrent.futures
import shutil
import subprocess
import sys
from pathlib import Path

SRC = "tb/tools/torture_campaign.py"
MUTANTS = [
    ("G01 bit-flip resolution removed",
     'if word is not None and word == audio_counter_word(tag, held["counter"] + 1):',
     'if False:'),
    ("G02 drop/repeat sign swapped",
     '"dropped" if shift > 0 else "repeated"', '"dropped" if shift < 0 else "repeated"'),
    ("G03 inserted silence never detected",
     'resumed = word is not None and self._own(channel, word) and \\',
     'resumed = False and \\'),
    ("G04 swap detection removed",
     'if partner is not None and partner != channel:', 'if False:'),
    ("G05 both-ends rule removed",
     'if any(half != {"dropped", "repeated", "bit-flip"} for half in halves):', 'if False:'),
    ("G06 missed arm no longer voids", "    if missed:\n        return \"NOT RUN\"",
     "    if False:\n        return \"NOT RUN\""),
    ("G07 capture loss needs only one channel",
     'if sorted({e["channel"] for e in hits}) != counter_channels:', 'if not hits:'),
    ("G08 arm tolerance widened by 100",
     'abs(event["capture_index"] - arm["index"]) > tolerance):',
     'abs(event["capture_index"] - arm["index"]) > tolerance + 100):'),
    ("G09 fast path compares one frame",
     'data[offset:offset + count * frame.size] == \\\n                    period[phase * frame.size:(phase + count) * frame.size]',
     'data[offset:offset + frame.size] == \\\n                    period[phase * frame.size:(phase + 1) * frame.size]'),
    ("G10 overflowing events pass",
     'if scan.unrecorded:\n        return "FAIL"', 'if False:\n        return "FAIL"'),
    ("G11 bit-flip arm mask not checked",
     'if event["n"] != 1 or event["mask"] != f"0x{arm[\'mask\']:08X}":', 'if event["n"] != 1:'),
    ("G12 swap partner channel ignored in a run",
     'run.get("partner") == partner', 'True'),
    ("S01 EARLY_TIMESTAMP dropped from zero growth",
     'RELEASE_ZERO_GROWTH_COUNTERS = ("SEQ_NUM_MISMATCH", "STREAM_INTERRUPTED",\n'
     '                                "LATE_TIMESTAMP", "EARLY_TIMESTAMP")',
     'RELEASE_ZERO_GROWTH_COUNTERS = ("SEQ_NUM_MISMATCH", "STREAM_INTERRUPTED",\n'
     '                                "LATE_TIMESTAMP")'),
    ("S02 unlock excused by any input's event",
     'matches = [event for event in unused',
     'matches = [event for event in sum(planted.values(), [])'),
    ("S03 counter decrease tolerated",
     '                if delta < 0:\n                    return "FAIL"',
     '                if delta < -1:\n                    return "FAIL"'),
    ("S04 one event excuses any number of unlocks",
     'if delta > len(matches):', 'if matches == [] and delta:'),
    ("R01 default-valued pre-cycle accepted",
     '    if at_default:\n        return "NOT RUN"', '    if False:\n        return "NOT RUN"'),
    ("R02 mixed commit state accepted",
     '        return "FAIL", dict(detail, why="mixed or partial state after a commit cut",',
     '        return "PASS", dict(detail, why="mixed or partial state after a commit cut",'),
    ("R03 soft reset graded as a commit cut",
     'snapshots = [pre, post, defaults] + ([committed] if phase == "journal_commit" else [])',
     'snapshots = [pre, post, defaults] + ([committed] if phase == "journal_commit" else [])\n'
     '    phase = "journal_commit" if phase == "soft_reset" and committed else phase'),
    ("E01 reset minimum not required for eligibility",
     '                                      and settings.reset_cycles >= minimum["soft_reset"]),',
     '                                      ),'),
    ("E02 audio eligibility ignores profile",
     '                          and _release_profile_eligible(settings)),', '                          ),'),
    ("E03 soak default back to seven days",
     'RELEASE_SOAK_DURATION_S = 24 * 60 * 60', 'RELEASE_SOAK_DURATION_S = 7 * 24 * 60 * 60'),
    ("E04 mix 110/40/50",
     'RELEASE_POWER_PHASES = (("idle", 100), ("journal_commit", 50), ("soft_reset", 50))',
     'RELEASE_POWER_PHASES = (("idle", 110), ("journal_commit", 40), ("soft_reset", 50))'),
    ("C01 persistence control restores everything",
     '"post": {item: "default" for item in items},', '"post": {item: "set" for item in items},'),
    ("C02 audio control loses its DUT drop",
     'events=fixture["source_events"] + [fixture["dut_event"]])',
     'events=fixture["source_events"])'),
    ("C03 first-boot control boots once",
     'desk_fixture={"boot_passes": 2, "restarts": 1, "capture_complete": True},',
     'desk_fixture={"boot_passes": 1, "restarts": 0, "capture_complete": True},'),
    ("A01 audio window rule not enforced",
     '        if self.audio_duration_s > self.soak_duration_s:\n            raise ValueError',
     '        if False:\n            raise ValueError'),
    ("A02 a sine-pair limit silently present",
     '"limits": None, "limits_status"', '"limits": {"thdn_db": -60}, "limits_status"'),
]


def run(root: Path, work: Path, index: int, mutant: tuple) -> tuple:
    name, old, new = mutant
    tree = work / f"m{index:02d}"
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(root, tree)
    path = tree / SRC
    text = path.read_text()
    if text.count(old) != 1:
        return name, "INVALID", f"anchor occurs {text.count(old)} times"
    path.write_text(text.replace(old, new))
    st = subprocess.run([sys.executable, "-B", SRC, "--self-test"], cwd=tree,
                        capture_output=True, text=True, timeout=900)
    bh = subprocess.run([sys.executable, "-B", "-m", "behave",
                         "tests/features/torture_campaign_plan.feature", "-f", "progress"],
                        cwd=tree, capture_output=True, text=True, timeout=900)
    verdict = "KILLED" if st.returncode or bh.returncode else "SURVIVED"
    return name, verdict, f"selftest rc={st.returncode} behave rc={bh.returncode}"


def main() -> int:
    root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    work.mkdir(parents=True, exist_ok=True)
    # Pristine control: both suites must pass on the unmodified copy.
    ctl = run(root, work, 99, ("CONTROL pristine", "RELEASE_SOAK_DURATION_S = 24 * 60 * 60",
                               "RELEASE_SOAK_DURATION_S = 24 * 60 * 60"))
    print(f"{ctl[0]}: {ctl[1]} ({ctl[2]})")
    with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
        results = list(pool.map(lambda a: run(root, work, *a), enumerate(MUTANTS)))
    for name, verdict, why in results:
        print(f"{verdict}: {name} ({why})")
    counts = {v: sum(1 for _, x, _ in results if x == v) for v in ("KILLED", "SURVIVED", "INVALID")}
    print(f"SUMMARY: {counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
