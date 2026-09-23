#!/usr/bin/env python3
"""Run one test_suite_cancellation.py revision against single-defect driver copies.

    mutate.py REPO SOURCE_REV TEST_REV SCRATCH OUT_DIR LABEL NAME[,NAME...]

Each copy is `git archive SOURCE_REV scripts` extracted into SCRATCH, with
scripts/test_suite_cancellation.py replaced by its blob at TEST_REV and exactly
one textual defect applied to scripts/run_all_suites.sh (the replaced text must
occur exactly once). The copy's own test is run from its own directory; the
fixture copies the production driver from that copy, not from REPO.
"""

import hashlib
import io
import json
import re
import subprocess
import sys
import tarfile
import time
from pathlib import Path

MUTANTS = {
    "none": None,
    # R257-2-F1 named defects.
    "logs-ready-early": ("LOGS_READY=0\ncancelled() {", "LOGS_READY=1\ncancelled() {"),
    "logs-ready-never-set": ('*.log || exit 2\n  LOGS_READY=1\n', '*.log || exit 2\n'),
    "no-partial-logs-message": ('    echo "partial logs: $OUT" >&2\n', '    :\n'),
    "no-term-trap": ("trap 'cancelled TERM 143' TERM\n", ""),
    # Further removals and corruptions of the same report.
    "no-int-trap": ("trap 'cancelled INT 130' INT\n", ""),
    "no-unprepared-message": ('    echo "logs were not prepared for this invocation" >&2\n', '    :\n'),
    "report-inverted": ('if [ "$LOGS_READY" = 1 ]; then', 'if [ "$LOGS_READY" != 1 ]; then'),
    "partial-logs-wrong-dir": ('echo "partial logs: $OUT" >&2', 'echo "partial logs: $ROOT/.suite-logs" >&2'),
    "int-reported-as-term": ("trap 'cancelled INT 130' INT", "trap 'cancelled TERM 130' INT"),
    "prepare-before-lock": ("  select_suites\n  acquire_lock\n  prepare_logs\n",
                            "  select_suites\n  prepare_logs\n  acquire_lock\n"),
}


def git(repo: str, *args: str) -> bytes:
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, check=True).stdout


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    repo, source_rev, test_rev, scratch, out_dir, label, names = sys.argv[1:8]
    source_rev = git(repo, "rev-parse", source_rev).decode().strip()
    test_rev = git(repo, "rev-parse", test_rev).decode().strip()
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    archive = git(repo, "archive", source_rev, "scripts")
    test = git(repo, "show", f"{test_rev}:scripts/test_suite_cancellation.py")
    results = []
    for name in names.split(","):
        copy = Path(scratch) / f"{label}-{name}"
        copy.mkdir(parents=True)
        with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
            tar.extractall(copy, filter="data")
        (copy / "scripts/test_suite_cancellation.py").write_bytes(test)
        driver = copy / "scripts/run_all_suites.sh"
        text = driver.read_text()
        defect = MUTANTS[name]
        if defect is not None:
            old, new = defect
            assert text.count(old) == 1, (name, text.count(old))
            driver.write_text(text.replace(old, new))
        began = time.monotonic()
        run = subprocess.run([sys.executable, str(copy / "scripts/test_suite_cancellation.py")],
                             cwd=copy, capture_output=True, text=True, timeout=900, check=False)
        seconds = round(time.monotonic() - began, 1)
        transcript = f"$ python3 scripts/test_suite_cancellation.py  (copy {label}-{name})\n" \
                     f"--- stdout ---\n{run.stdout}--- stderr ---\n{run.stderr}exit {run.returncode}\n"
        (out / f"{label}-{name}.txt").write_text(transcript)
        arms = re.findall(r"^([a-z][A-Za-z0-9-]*): \{", run.stdout, re.M)
        frames = re.findall(r'File "[^"]*/scripts/(test_suite_cancellation\.py)", line (\d+), in (\w+)',
                            run.stderr)
        error = next((line for line in run.stderr.splitlines() if line.startswith("AssertionError")), "")
        results.append(dict(
            mutant=name, defect=defect, exit=run.returncode,
            verdict=("PASS" if run.returncode == 0 else "RED"),
            seconds=seconds, arms_passed=len(arms), last_passed_arm=arms[-1] if arms else None,
            failing_frames=[f"{f}:{n} {fn}" for f, n, fn in frames],
            assertion_first_line=error[:200],
            driver_sha256=sha(driver.read_bytes()), test_sha256=sha(test),
            source_rev=source_rev, test_rev=test_rev))
        print(f"{label:>5} {name:<26} exit {run.returncode:>3}  {seconds:>6}s  "
              f"{results[-1]['failing_frames'][-1:] or ''}", flush=True)
    (out / f"{label}-results.json").write_text(json.dumps(results, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
