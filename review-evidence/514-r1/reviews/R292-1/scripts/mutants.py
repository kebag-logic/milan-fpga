#!/usr/bin/env python3
"""Reviewer mutation probes for PR #552 (#514) against the shipped self-test.

    python3 -B mutants.py list
    python3 -B mutants.py run SOURCE_CLONE SCRATCH_DIR MUTANT_ID

`run` makes a disposable shared clone of SOURCE_CLONE at its HEAD under
SCRATCH_DIR/<id>, applies exactly one textual mutation (the `before` text must
occur exactly once), runs `check_merge_containment.py --selftest` there and
prints: id, exit code, number of FAIL lines, the first FAIL lines.
KILLED means the self-test exits nonzero or reports a FAIL.
"""
import subprocess
import sys
from pathlib import Path

R = "scripts/merge_containment_replay.py"
C = "scripts/check_merge_containment.py"
MUTANTS = {
    "M01-ancestry-note-dropped": (C,
        'return (True, 0, "historical inclusion by ancestry; current retention not implied")',
        "return (True, 0, None)"),
    "M02-linear-note-unqualified": (C,
        'f"historical inclusion only: every commit has a whitespace-exact equivalent in "',
        'f"every commit has a whitespace-exact equivalent in "'),
    "M03-retention-unknown-not-counted": (C,
        "unknown += not retained", "pass"),
    "M04-retention-word-always-retained": (C,
        'word = "retained" if retained else "UNKNOWN"', 'word = "retained"'),
    "M05-option-ignored": (C,
        'current_retention = "--current-retention" in args',
        "current_retention = False"),
    "M06-option-dup-check-removed": (C,
        '("--selftest", "--base", "--merged-prs", "--no-fetch", "--current-retention")',
        '("--selftest", "--base", "--merged-prs", "--no-fetch")'),
    "M07-missing-ignored": (R,
        "    if missing:\n        return False, \"unproved on: \"",
        "    if False:\n        return False, \"unproved on: \""),
    "M08-one-merge-allowed": (R,
        "if int(merges) != 0:", "if int(merges) > 1:"),
    "M09-H-measurement-failure-certifies": (R,
        "        if matched is None:\n            raise _MeasurementError(error)\n        if not matched:",
        "        if matched is None:\n            matched = True\n        if not matched:"),
    "M10-measurement-error-certifies": (R,
        '        return False, f"linear retention unmeasurable: {exc}"',
        '        return True, f"linear retention unmeasurable: {exc}"'),
    "M11-merge-count-parse-guard-removed": (R,
        '        if not merges.isdigit():\n            raise _MeasurementError("invalid source merge count")\n',
        ""),
    "M12-retention-on-stranded": (C,
        "            stranded += 1\n",
        "            stranded += 1\n            if current_retention:\n"
        "                print(f\"  retained   {label}: current retention: mutant\")\n"),
    "M13-summary-requested-proof-wording": (C,
        'print(f"{unknown} tip(s) lack a requested proof; see UNKNOWN above.")',
        'print(f"{unknown} tip(s) lack a containment proof; see UNKNOWN above.")'),
    "M14-historical-linear-verdict-withdrawn": (C,
        "        if equivalent:\n            return (True, ahead,",
        "        if equivalent and False:\n            return (True, ahead,"),
    "M15-H-refusal-falls-through-to-T": (R,
        "        if not matched:\n            return False, \"unsupported: needs",
        "        if not matched and False:\n            return False, \"unsupported: needs"),
}


def run(source, scratch, ident):
    path, before, after = MUTANTS[ident]
    work = Path(scratch) / ident
    subprocess.run(["git", "clone", "-q", "--shared", source, str(work)], check=True)
    target = work / path
    data = target.read_text(encoding="utf-8")
    if data.count(before) != 1:
        print(f"{ident} INVALID mutation site count {data.count(before)}")
        return 2
    target.write_text(data.replace(before, after), encoding="utf-8")
    p = subprocess.run([sys.executable, "-B", "scripts/check_merge_containment.py",
                        "--selftest"], cwd=work, capture_output=True, text=True)
    out = p.stdout + p.stderr
    fails = [line.strip() for line in out.splitlines() if line.lstrip().startswith("FAIL")]
    verdict = "KILLED" if (p.returncode != 0 or fails) else "SURVIVED"
    print(f"{ident} {verdict} exit={p.returncode} fails={len(fails)}")
    for line in fails[:6]:
        print(f"    {line[:200]}")
    if p.returncode != 0 and not fails:
        print("    tail: " + " | ".join(out.strip().splitlines()[-3:])[:300])
    return 0


if __name__ == "__main__":
    if sys.argv[1] == "list":
        print("\n".join(MUTANTS))
    else:
        sys.exit(run(*sys.argv[2:5]))
