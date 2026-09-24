#!/usr/bin/env python3
"""Round-2 reviewer mutants aimed at the cases added at b0347a4f.

    python3 -B round2_mutants.py HEAD_SCRIPTS_DIR SCRATCH_DIR GIT_REPO OUT.json [JOBS]

Same method as mutation_probe.py: one exact, single-occurrence byte
replacement in a disposable copy, then the copy's full --selftest with cwd
GIT_REPO. KILLED = non-zero exit; SURVIVED = "selftest: PASS" with exit 0.
Each row names the round-2 case(s) expected to kill it. An unmutated control
must pass. At most JOBS (default 8, capped at 8) run at once.
"""
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SRC, SCRATCH, REPO, OUT = (Path(a).resolve() for a in sys.argv[1:5])
JOBS = min(int(sys.argv[5]) if len(sys.argv) > 5 else 8, 8)
R = "merge_containment_replay.py"
C = "check_merge_containment.py"
RET_CALL = (b"            if current_retention:\n"
            b"                retained, detail = linear_retention_verdict(ref, base, _git, _linear_patches_contained)\n"
            b"                word = \"retained\" if retained else \"UNKNOWN\"\n"
            b"                print(f\"  {word:<10} {label}: current retention: {detail}\")\n"
            b"                unknown += not retained\n")
STRANDED_TAIL = b"            stranded += 1\n"

MUTANTS = [
    # name, file, before, after, expected killer (documentation only)
    ("control-unmutated", None, b"", b"", "-"),
    ("empty-delta-certified", R,
     b'        raise _MeasurementError("retention has no measurable changed-path set")',
     b"        return []", "linear-empty-delta"),
    ("H-error-as-unsupported", R,
     b"if matched is None:\n            raise _MeasurementError(error)",
     b'if matched is None:\n            return False, "unsupported: needs a nonempty whitespace-exact linear replay"',
     "linear-H-failure-diagnostic (collides with a self-test guard string; see non-colliding variant)"),
    ("H-error-as-unsupported-noncolliding", R,
     b"if matched is None:\n            raise _MeasurementError(error)",
     b'if matched is None:\n            return False, "unsupported: H unavailable"',
     "linear-H-failure-diagnostic"),
    ("H-error-silently-matched-empty-missing", R,
     b"if matched is None:\n            raise _MeasurementError(error)",
     b"if matched is None:\n            return True, error",
     "linear-H-measurement-failure"),
    ("unknown-ref-prints-retained", C,
     b'            print(f"  UNKNOWN    {label}: {note}")\n',
     b'            print(f"  UNKNOWN    {label}: {note}")\n'
     b'            if current_retention:\n'
     b'                print(f"  retained   {label}: current retention: mutant")\n',
     "linear-no-retained-on-UNKNOWN"),
    ("pre-error-prints-retained", C,
     b'            print(f"  UNKNOWN    {label}: {pre_error}")\n',
     b'            print(f"  UNKNOWN    {label}: {pre_error}")\n'
     b'            if current_retention:\n'
     b'                print(f"  retained   {label}: current retention: mutant")\n',
     "(reachable only through a --merged-prs pre-error)"),
    ("retention-also-evaluated-when-stranded", C, STRANDED_TAIL,
     STRANDED_TAIL + RET_CALL, "linear-no-retention-on-STRANDED"),
    ("stranded-prints-unknown-retention", C, STRANDED_TAIL,
     STRANDED_TAIL + b"            if current_retention:\n"
     b'                print(f"  UNKNOWN    {label}: current retention: not evaluated")\n',
     "linear-no-retention-on-STRANDED"),
    ("ancestry-disclaimer-dropped", C,
     b'"historical inclusion by ancestry; current retention not implied"',
     b'"historical inclusion by ancestry"', "linear-ancestry-*-claim"),
    ("ancestry-historical-dropped", C,
     b'"historical inclusion by ancestry; current retention not implied"',
     b'"ancestor; current retention not implied"', "linear-ancestry-*-claim"),
    ("retained-claim-replay-dropped", R,
     b'f"raw no-op retention at {target}; historical linear replay proved"',
     b'f"raw no-op retention at {target}"', "linear-*-retained-claim"),
    ("retained-claim-target-dropped", R,
     b'f"raw no-op retention at {target}; historical linear replay proved"',
     b'f"historical linear replay proved"', "linear-*-retained-claim"),
    ("retained-line-printed-twice", C,
     b'                print(f"  {word:<10} {label}: current retention: {detail}")\n',
     b'                print(f"  {word:<10} {label}: current retention: {detail}")\n'
     b'                print(f"  {word:<10} {label}: current retention: {detail}")\n',
     "linear-*-retained-claim (exactly one line)"),
]


def run(mutant):
    name, target, before, after, killer = mutant
    work = SCRATCH / name
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(SRC, work)
    if target:
        path = work / target
        data = path.read_bytes()
        if data.count(before) != 1:
            return {"mutant": name, "status": "NOT-APPLIED",
                    "detail": f"{data.count(before)} occurrences", "expected_killer": killer}
        path.write_bytes(data.replace(before, after))
    p = subprocess.run([sys.executable, "-B", str(work / C), "--selftest"],
                       cwd=REPO, capture_output=True, text=True, errors="backslashreplace")
    fails = [l.strip() for l in p.stdout.splitlines() if l.startswith("  FAIL")]
    passed = p.returncode == 0 and "selftest: PASS" in p.stdout
    status = ("PASS" if passed else "FAIL") if not target else (
        "SURVIVED" if passed else "KILLED")
    (SCRATCH / f"{name}.log").write_text(p.stdout + "\n--stderr--\n" + p.stderr)
    return {"mutant": name, "file": target, "rc": p.returncode, "status": status,
            "expected_killer": killer, "failing_cases": [f.split()[1] for f in fails][:12],
            "failing_count": len(fails), "stderr_tail": p.stderr.strip().splitlines()[-1:]}


def main():
    SCRATCH.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(JOBS) as pool:
        rows = list(pool.map(run, MUTANTS))
    for r in rows:
        print(f"{r['status']:<11} {r['mutant']:<40} rc={r.get('rc')} fails={r.get('failing_count')} "
              f"expected={r['expected_killer']} got={r.get('failing_cases', [])[:4]}")
    OUT.write_text(json.dumps(rows, indent=1))
    control_ok = rows[0]["status"] == "PASS"
    applied = all(r["status"] != "NOT-APPLIED" for r in rows)
    print("CONTROL", "PASS" if control_ok else "FAIL", "| ALL APPLIED", applied)
    return 0 if control_ok and applied else 1


if __name__ == "__main__":
    sys.exit(main())
