#!/usr/bin/env python3
"""Disposable planted-defect probes for PR #782 round 2.

Each mutant is an exact text substitution on a `git archive` copy of the
reviewed head under <scratch>/mut/<name>. The copy then runs the gate named
for that mutant; a mutant is CAUGHT when the gate exits non-zero, ESCAPES
when it exits zero. Expected outcomes are stated per mutant and compared.

    python3 mutants.py <clone> <head-sha> <scratch-dir> <receipt-dir>
"""
import concurrent.futures as cf
import shutil
import subprocess
import sys
from pathlib import Path

CLONE, HEAD, SCRATCH, OUT = (Path(sys.argv[1]), sys.argv[2],
                             Path(sys.argv[3]), Path(sys.argv[4]))
SS = "scripts/suite_shards.py"
RA = "scripts/run_all_suites.sh"
SELFTEST = ["python3", "-E", "-s", SS, "--selftest"]
CONTRACT = ["python3", "-E", "-s", "scripts/measure_test_evidence.py", "--check"]
EMPTY = "PROVISIONAL_SUITES: frozenset[str] = frozenset()"
FIG = '    "media_phase": 1400,'
ARM = 'media_phase)       printf \'%s\\n\' "${SUITE_TIMEOUT:-1400}" ;;'

# name: (expected, gate, [(path, old, new), ...], what it plants)
MUTANTS = {
    "control": ("ESCAPE", SELFTEST, [], "unmodified head"),
    "m1_figure_582": ("ESCAPE", SELFTEST, [(SS, FIG, '    "media_phase": 582,')],
                      "measured suite's figure lowered to its 582 s window "
                      "(the stated open risk)"),
    "m2_figure_1401": ("ESCAPE", SELFTEST, [(SS, FIG, '    "media_phase": 1401,')],
                       "figure one second above its own 1400 s deadline"),
    "m3_prov_582": ("CAUGHT", SELFTEST,
                    [(SS, FIG, '    "media_phase": 582,'),
                     (SS, EMPTY, 'PROVISIONAL_SUITES: frozenset[str] = frozenset({"media_phase"})')],
                    "582 s left provisional"),
    "m4_prov_1400": ("ESCAPE", SELFTEST,
                     [(SS, EMPTY, 'PROVISIONAL_SUITES: frozenset[str] = frozenset({"media_phase"})')],
                     "media_phase still provisional at 1400 s (round-1 state; self-consistent)"),
    "m5_prov_misspelt": ("CAUGHT", SELFTEST,
                         [(SS, EMPTY, 'PROVISIONAL_SUITES: frozenset[str] = frozenset({"media_phse"})')],
                         "misspelt provisional name"),
    "m6_compare_disabled": ("CAUGHT", SELFTEST,
                            [(SS, "        elif seconds[suite] != expected:",
                              "        elif False:")],
                            "provisional comparison disabled while nothing is pending"),
    "m7_head_count_dropped": ("CAUGHT", SELFTEST,
                              [(SS, "    if problems or provisional:", "    if problems:"),
                               (SS, FIG, '    "media_phase": 582,'),
                               (SS, EMPTY, 'PROVISIONAL_SUITES: frozenset[str] = frozenset({"media_phase"})')],
                              "head arm stops counting a provisional mismatch"),
    "m8_figure_1499": ("CAUGHT", SELFTEST, [(SS, FIG, '    "media_phase": 1499,')],
                       "figure at 1499 s, over a regular worker's 1498 s"),
    "m9_driver_582": ("CAUGHT", CONTRACT,
                      [(RA, ARM, ARM.replace("1400", "582"))],
                      "driver deadline lowered to 582 s"),
    "m10_driver_900": ("CAUGHT", CONTRACT,
                       [(RA, ARM, ARM.replace("1400", "900"))],
                       "driver deadline back at 900 s"),
}


def build(name: str) -> Path:
    tree = SCRATCH / "mut" / name
    shutil.rmtree(tree, ignore_errors=True)
    tree.mkdir(parents=True)
    archive = subprocess.run(["git", "-C", str(CLONE), "archive", HEAD],
                             check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(tree)], input=archive, check=True)
    return tree


def run(name: str) -> tuple[str, str, str, int, str]:
    expected, gate, edits, what = MUTANTS[name]
    tree = build(name)
    for rel, old, new in edits:
        path = tree / rel
        text = path.read_text(encoding="utf-8")
        if text.count(old) != 1:
            return name, expected, "NOT-APPLIED", -1, what
        path.write_text(text.replace(old, new), encoding="utf-8")
    proc = subprocess.run(gate, cwd=tree, capture_output=True, text=True)
    (OUT / f"{name}.log").write_text(proc.stdout + proc.stderr, encoding="utf-8")
    got = "CAUGHT" if proc.returncode else "ESCAPE"
    return name, expected, got, proc.returncode, what


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(max_workers=11) as pool:
        rows = list(pool.map(run, MUTANTS))
    bad = 0
    lines = []
    for name, expected, got, rc, what in rows:
        ok = expected == got
        bad += not ok
        lines.append(f"{'ok  ' if ok else 'MISS'} {name:24} expected {expected:6} got {got:11} rc={rc}  {what}")
    lines.append(f"mutants: {len(rows)}  as expected: {len(rows) - bad}")
    (OUT / "SUMMARY.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
