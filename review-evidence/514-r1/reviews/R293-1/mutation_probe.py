#!/usr/bin/env python3
"""Reviewer mutation probe for #514: does the head self-test kill each mutant?

    python3 -B mutation_probe.py HEAD_SCRIPTS_DIR SCRATCH_DIR GIT_REPO OUT.json [JOBS]

Each mutant is one exact, single-occurrence byte replacement in a disposable
copy of HEAD_SCRIPTS_DIR. The copy's `check_merge_containment.py --selftest`
runs with cwd GIT_REPO (the checker needs a repository for its graft check;
the self-test works in its own scratch directories). KILLED means the
self-test exited non-zero; SURVIVED means it still printed PASS with exit 0.
An unmutated control copy must pass. At most JOBS (default 8) run at once.
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

MUTANTS = [
    ("control-unmutated", None, b"", b""),
    ("T-bypass", R, b"missing = _retained_at_tip(source, target, git)", b"missing = []"),
    ("shape-guard-off", R, b"if int(merges) != 0:", b"if False:"),
    ("merge-count-digit-guard-off", R, b"if not merges.isdigit():\n            raise",
     b"if False:\n            raise"),
    ("H-unmatched-accepted", R, b"if not matched:\n            return False",
     b"if False:\n            return False"),
    ("H-error-ignored", R, b"if matched is None:\n            raise _MeasurementError(error)",
     b"if matched is None:\n            matched = True"),
    ("measurement-except-certifies", R,
     b'return False, f"linear retention unmeasurable: {exc}"',
     b'return True, f"linear retention unmeasurable: {exc}"'),
    ("missing-list-ignored", R, b"    if missing:\n        return False",
     b"    if False:\n        return False"),
    ("retained-diagnostic-blank", R,
     b'return True, f"raw no-op retention at {target}; historical linear replay proved"',
     b'return True, ""'),
    ("report-unknown-not-counted", C, b"unknown += not retained", b"unknown += 0"),
    ("report-word-always-retained", C,
     b'word = "retained" if retained else "UNKNOWN"', b'word = "retained"'),
    ("option-never-enabled", C, b'current_retention = "--current-retention" in args',
     b"current_retention = False"),
    ("option-dup-check-dropped", C,
     b'for flag in ("--selftest", "--base", "--merged-prs", "--no-fetch", "--current-retention"):',
     b'for flag in ("--selftest", "--base", "--merged-prs", "--no-fetch"):'),
    ("ancestry-diagnostic-dropped", C,
     b'return (True, 0, "historical inclusion by ancestry; current retention not implied")',
     b"return (True, 0, None)"),
    ("linear-diagnostic-historical-dropped", C,
     b'f"historical inclusion only: every commit has', b'f"every commit has'),
    ("retention-uses-default-arm-verdict", C,
     b"retained, detail = linear_retention_verdict(ref, base, _git, _linear_patches_contained)",
     b"retained, detail = (True, str(note))"),
    ("mode-rule-dropped", R,
     b"    if not (tip[0] == branch[0]\n            or (original is not None and original[0] == branch[0])):\n        return False",
     b"    if False:\n        return False"),
]


def run(mutant):
    name, target, before, after = mutant
    work = SCRATCH / name
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(SRC, work)
    if target:
        path = work / target
        data = path.read_bytes()
        if data.count(before) != 1:
            return {"mutant": name, "status": "NOT-APPLIED",
                    "detail": f"{data.count(before)} occurrences"}
        path.write_bytes(data.replace(before, after))
    p = subprocess.run([sys.executable, "-B", str(work / C), "--selftest"],
                       cwd=REPO, capture_output=True, text=True, errors="backslashreplace")
    fails = [l.strip() for l in p.stdout.splitlines() if l.startswith("  FAIL")]
    passed = p.returncode == 0 and "selftest: PASS" in p.stdout
    status = ("PASS" if passed else "FAIL") if not target else (
        "SURVIVED" if passed else "KILLED")
    (SCRATCH / f"{name}.log").write_text(p.stdout + "\n--stderr--\n" + p.stderr)
    return {"mutant": name, "file": target, "before": before.decode(),
            "after": after.decode(), "rc": p.returncode, "status": status,
            "failing_cases": fails[:12], "failing_count": len(fails)}


def main():
    SCRATCH.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(JOBS) as pool:
        rows = list(pool.map(run, MUTANTS))
    for r in rows:
        print(f"{r['status']:<11} {r['mutant']:<38} rc={r.get('rc')} "
              f"fails={r.get('failing_count')} {r.get('failing_cases', [])[:3]}")
    OUT.write_text(json.dumps(rows, indent=1))
    control_ok = rows[0]["status"] == "PASS"
    applied = all(r["status"] != "NOT-APPLIED" for r in rows)
    print("CONTROL", "PASS" if control_ok else "FAIL", "| ALL APPLIED", applied)
    return 0 if control_ok and applied else 1


if __name__ == "__main__":
    sys.exit(main())
