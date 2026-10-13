#!/usr/bin/env python3
"""Apply the selector docstring's new-suite steps 1 and 2 to a disposable copy.

usage: python3 -I new_suite_steps.py COPY step1|step2

Every edit is an exact replacement that must match once, and each is printed
with the docstring sentence it carries out.
"""
import sys
from pathlib import Path

SEL = "scripts/suite_shards.py"
WF = ".github/workflows/rtl.yml"
CI = "scripts/ci_events.py"
STEP1 = [
    ("Add the suite to SUITE_SECONDS at the wall clock that suite_timeout gives it "
     "(no own arm, so the `*` arm: 1800 s)", SEL,
     '    "tsn_fuzz": 60,\n}\n', '    "tsn_fuzz": 60,\n    "zz_new_suite": 1800,\n}\n'),
    ("Name it in PROVISIONAL_SUITES", SEL,
     "PROVISIONAL_SUITES: frozenset[str] = frozenset()\n",
     'PROVISIONAL_SUITES: frozenset[str] = frozenset({"zz_new_suite"})\n'),
]
OWN = 'test "$(cat "$RUNNER_TEMP/owned-suites")" = milan_dp ;;'
STEP2 = [
    ("rtl.yml: append the new last index to the verilator-shards matrix's shard, "
     "set its total to the new count", WF,
     "        shard: [0, 1, 2, 3, 4]\n        total: [5]\n",
     "        shard: [0, 1, 2, 3, 4, 5]\n        total: [6]\n"),
    ("rtl.yml: set the verilator-suites verifier's --expect to the new count", WF,
     "python3 scripts/ci_events.py --require-target-sha --expect 5 \\\n",
     "python3 scripts/ci_events.py --require-target-sha --expect 6 \\\n"),
    ("rtl.yml: give the ownership step's milan_dp arm the new last index", WF,
     f"            4) {OWN}\n", f"            5) {OWN}\n"),
    ("ci_events.py: the same change to CANONICAL_OWNERSHIP_SCRIPT", CI,
     f"    '4) {OWN}',\n", f"    '5) {OWN}',\n"),
    ("ci_events.py: the same change to the canonical verilator-suites verifier step", CI,
     "             'python3 scripts/ci_events.py --require-target-sha --expect 5 --sha '",
     "             'python3 scripts/ci_events.py --require-target-sha --expect 6 --sha '"),
    ("ci_events.py self-test: _m_shard_denominator_stale's asserted shard list, "
     "restated count and planted index", CI,
     '    assert shard == [0, 1, 2, 3, 4], "fixture drift: verilator-shards matrix"\n'
     '    _restate_shards(w, "verilator-shards", "5")\n    shard.append(5)\n',
     '    assert shard == [0, 1, 2, 3, 4, 5], "fixture drift: verilator-shards matrix"\n'
     '    _restate_shards(w, "verilator-shards", "6")\n    shard.append(6)\n'),
    ("ci_events.py self-test: _m_dedicated_worker_dropped's asserted last index", CI,
     '    assert shard[-1] == 4, "fixture drift: verilator-shards matrix"\n    shard.pop()\n',
     '    assert shard[-1] == 5, "fixture drift: verilator-shards matrix"\n    shard.pop()\n'),
    ("ci_events.py self-test: _m_dedicated_worker_reverted's asserted last index "
     "and planted count", CI,
     '    assert matrix["shard"][-1] == 4, "fixture drift: verilator-shards matrix"\n'
     '    matrix["shard"].pop()\n    matrix["total"] = [4]\n',
     '    assert matrix["shard"][-1] == 5, "fixture drift: verilator-shards matrix"\n'
     '    matrix["shard"].pop()\n    matrix["total"] = [5]\n'),
    ("ci_events.py self-test: _m_ownership_dedicated_arm_dropped's asserted arm index", CI,
     f"    arm = '4) {OWN}'\n", f"    arm = '5) {OWN}'\n"),
    ("ci_events.py self-test: _m_shard_matrix_include's planted index and count", CI,
     '    ] = [{"shard": 4, "total": 5}]\n', '    ] = [{"shard": 5, "total": 6}]\n'),
    ("ci_events.py self-test: _m_verify_expect_missing's asserted count", CI,
     '    assert "--expect 5 " in s["run"]\n    s["run"] = s["run"].replace("--expect 5 ", "")\n',
     '    assert "--expect 6 " in s["run"]\n    s["run"] = s["run"].replace("--expect 6 ", "")\n'),
    ("ci_events.py self-test: _m_matrix_grows_expect_stays's asserted shard list "
     "and planted index", CI,
     '    assert shard == [0, 1, 2, 3, 4], "fixture drift: verilator-shards matrix"\n'
     '    shard.append(5)\n',
     '    assert shard == [0, 1, 2, 3, 4, 5], "fixture drift: verilator-shards matrix"\n'
     '    shard.append(6)\n'),
    ("ci_events.py self-test: the expected finding of 'R4 matrix grows, --expect stays'", CI,
     '        ("R4 matrix grows, --expect stays", _m_matrix_grows_expect_stays,\n'
     '         "--expect 6"),\n',
     '        ("R4 matrix grows, --expect stays", _m_matrix_grows_expect_stays,\n'
     '         "--expect 7"),\n'),
    ("ci_events.py self-test: the expected finding of '#444 the matrix and total "
     "return to four, --expect stays'", CI,
     '         _m_dedicated_worker_reverted, "--expect 4"),\n',
     '         _m_dedicated_worker_reverted, "--expect 5"),\n'),
    ("this file: give the self-test's milan_dp landmark the new last index", SEL,
     '    landmarks = {"tsn_fuzz": 1, "chmap_capture": 3, "milan_dp": 4}\n',
     '    landmarks = {"tsn_fuzz": 1, "chmap_capture": 3, "milan_dp": 5}\n'),
    ("this file: one more WORKER_OVERHEAD_SECONDS entry before the last, equal to "
     "the largest one already there (115)", SEL,
     "WORKER_OVERHEAD_SECONDS = (83, 115, 80, 93, 80)\n",
     "WORKER_OVERHEAD_SECONDS = (83, 115, 80, 93, 115, 80)\n"),
]


def main(argv: list[str]) -> int:
    """Apply one step's edits to the copy at argv[1]."""
    copy, step = Path(argv[1]), {"step1": STEP1, "step2": STEP2}[argv[2]]
    for sentence, rel, old, new in step:
        path = copy / rel
        text = path.read_text(encoding="utf-8")
        if text.count(old) != 1:
            print(f"DRIFT {rel}: {sentence}")
            return 1
        path.write_text(text.replace(old, new), encoding="utf-8")
        print(f"applied {rel}: {sentence}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
