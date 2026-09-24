#!/usr/bin/env python3
"""Round-2 reviewer equivalents for PR #552 (#514) against the shipped self-test.

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
    "M16-retention-on-pre-error-unknown": (C,
        '            print(f"  UNKNOWN    {label}: {pre_error}")\n',
        '            print(f"  UNKNOWN    {label}: {pre_error}")\n'
        '            if current_retention:\n'
        '                print(f"  retained   {label}: current retention: mutant")\n'),
    "M17-retention-on-contained-unknown": (C,
        '            print(f"  UNKNOWN    {label}: {note}")\n',
        '            print(f"  UNKNOWN    {label}: {note}")\n'
        '            if current_retention:\n'
        '                print(f"  retained   {label}: current retention: mutant")\n'),
    "M18-ancestry-disclaimer-dropped": (C,
        '"historical inclusion by ancestry; current retention not implied"',
        '"historical inclusion by ancestry"'),
    "M19-empty-delta-certifies": (R,
        '        raise _MeasurementError("retention has no measurable changed-path set")',
        '        return []'),
    "M20-retained-detail-unqualified": (R,
        'return True, f"raw no-op retention at {target}; historical linear replay proved"',
        'return True, f"retained at {target}"'),
    "M21-H-failure-reported-as-unsupported": (R,
        '        if matched is None:\n            raise _MeasurementError(error)\n        if not matched:',
        '        if matched is None:\n            return False, "unsupported: needs"\n        if not matched:'),
    "M22-real-retention-on-stranded": (C,
        "            stranded += 1\n",
        "            stranded += 1\n            if current_retention:\n"
        "                retained, detail = linear_retention_verdict(ref, base, _git, _linear_patches_contained)\n"
        "                print(f\"  {'retained' if retained else 'UNKNOWN':<10} {label}: current retention: {detail}\")\n"),
    "M23-empty-delta-guard-after-H-skipped": (R,
        '        missing = _retained_at_tip(source, target, git)\n    except',
        '        missing = []\n    except'),
    "M24-retained-detail-blank": (R,
        'return True, f"raw no-op retention at {target}; historical linear replay proved"',
        'return True, ""'),
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
