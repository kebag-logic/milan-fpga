"""Plant mutants of scripts/act_ci.py in scratch copies and run each copy's offline self-test.

Usage: python3 -I mutants.py <checkout> <scratch-dir> <receipt-dir>

Each mutant is one exact text replacement that must match once. Every copy,
including the unmutated control, is installed mode 0555 and run as
`python3 -I <copy> --selftest --worktree <checkout>`; the FAIL lines and rc
are recorded per mutant. A mutant is killed when rc != 0 and at least one
named check fails that the control passes.
"""
import concurrent.futures
import json
import os
import pathlib
import subprocess
import sys

MUTANTS = {
    "control": [],
    "drop-2404-from-platform-map": [(
        'for label in RUNS_ON_LABELS for word in ("--platform", f"{label}={RUNNER_IMAGE}")',
        'for label in ("ubuntu-latest",) for word in ("--platform", f"{label}={RUNNER_IMAGE}")',
    )],
    "map-2404-to-act-default-image": [(
        'for label in RUNS_ON_LABELS for word in ("--platform", f"{label}={RUNNER_IMAGE}")',
        'for label in RUNS_ON_LABELS for word in ("--platform", f"{label}={RUNNER_IMAGE if label == \'ubuntu-latest\' else \'node:16-bullseye-slim\'}")',
    )],
    "sandbox-accepts-any-ubuntu-prefix": [(
        "            if runs_on not in RUNS_ON_LABELS:\n",
        "            if not (isinstance(runs_on, str) and runs_on.startswith('ubuntu-')):\n",
    )],
    "sandbox-accepts-one-label-list": [(
        "            if runs_on not in RUNS_ON_LABELS:\n",
        "            if runs_on not in RUNS_ON_LABELS and not (isinstance(runs_on, list) and runs_on[:1] == ['ubuntu-24.04']):\n",
    )],
    "sandbox-case-insensitive": [(
        "            if runs_on not in RUNS_ON_LABELS:\n",
        "            if str(runs_on).lower() not in RUNS_ON_LABELS:\n",
    )],
    "third-label-2204-added": [(
        'RUNS_ON_LABELS = ("ubuntu-latest", "ubuntu-24.04")',
        'RUNS_ON_LABELS = ("ubuntu-latest", "ubuntu-24.04", "ubuntu-22.04")',
    )],
    "platform-map-duplicated": [(
        'for label in RUNS_ON_LABELS for word in ("--platform", f"{label}={RUNNER_IMAGE}")',
        'for label in RUNS_ON_LABELS * 2 for word in ("--platform", f"{label}={RUNNER_IMAGE}")',
    )],
    "run-validation-skips-sandbox": [(
        "        validate_workflow_sandbox(layout.checkout, workflows)\n        job_volume_scope",
        "        job_volume_scope",
    )],
    "sandbox-accepts-only-2404-drops-latest": [(
        "            if runs_on not in RUNS_ON_LABELS:\n",
        "            if runs_on != 'ubuntu-24.04':\n",
    )],
}


def main() -> int:
    checkout, scratch, receipts = (pathlib.Path(arg).resolve() for arg in sys.argv[1:4])
    source = (checkout / "scripts" / "act_ci.py").read_text(encoding="utf-8")
    receipts.mkdir(parents=True, exist_ok=True)
    jobs = {}
    for name, edits in MUTANTS.items():
        text = source
        for old, new in edits:
            if text.count(old) != 1:
                raise SystemExit(f"{name}: pattern matched {text.count(old)} times")
            text = text.replace(old, new)
        directory = scratch / f"mutant-{name}"
        directory.mkdir(parents=True, exist_ok=True)
        copy = directory / "act_ci.py"
        if copy.exists():
            copy.chmod(0o644)
        copy.write_text(text, encoding="utf-8")
        copy.chmod(0o555)
        jobs[name] = copy

    def run(name: str) -> tuple[str, int, list[str]]:
        result = subprocess.run(
            [sys.executable, "-I", str(jobs[name]), "--selftest", "--worktree", str(checkout)],
            capture_output=True, text=True, cwd=scratch,
        )
        (receipts / f"{name}.log").write_text(result.stdout + result.stderr, encoding="utf-8")
        fails = [line.strip() for line in (result.stdout + result.stderr).splitlines()
                 if line.lstrip().startswith("FAIL")]
        return name, result.returncode, fails

    with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(jobs), 10)) as pool:
        results = {name: (rc, fails) for name, rc, fails in pool.map(run, jobs)}
    control_rc, control_fails = results["control"]
    summary = {}
    for name, (rc, fails) in results.items():
        new = sorted(set(fails) - set(control_fails))
        killed = name != "control" and rc != 0 and bool(new)
        summary[name] = {"rc": rc, "fail_count": len(fails), "new_failures": new,
                         "verdict": "control" if name == "control" else ("KILLED" if killed else "SURVIVED")}
    (receipts / "summary.json").write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
    for name, row in summary.items():
        print(f"{row['verdict']:8} rc={row['rc']} fails={row['fail_count']} {name}")
        for line in row["new_failures"]:
            print(f"           {line}")
    survived = [n for n, r in summary.items() if r["verdict"] == "SURVIVED"]
    return 1 if survived or control_rc != 0 else 0


if __name__ == "__main__":
    sys.exit(main())
