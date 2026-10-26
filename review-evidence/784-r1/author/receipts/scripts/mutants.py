#!/usr/bin/env python3
"""Plant one mutant of scripts/act_ci.py in a scratch copy and run its isolated self-test.

usage: mutants.py <checkout> <receipt-dir> <mutant-name>...

Each mutant is an exact, single-occurrence replacement. The copy runs as the
runner contract gate's second command does: python3 -I <copy> --selftest
--worktree <checkout>. The receipt records the replacement, the exit status and
every FAIL line, with the scratch path replaced by <copy>.
"""

import json
import pathlib
import subprocess
import sys
import tempfile

PLATFORMS_NEW = (
    '        *(word for label in RUNS_ON_LABELS for word in ("--platform", f"{label}={RUNNER_IMAGE}")),\n'
)
MUTANTS = {
    # The assignment's mutant: the platform map loses the new label (dev's form).
    "drop-2404-from-platform-map": (
        PLATFORMS_NEW,
        '        "--platform",\n        f"ubuntu-latest={RUNNER_IMAGE}",\n',
    ),
    # The new label maps to act's own default image instead of the runner image.
    "map-2404-to-act-default-image": (
        PLATFORMS_NEW,
        '        "--platform",\n        f"ubuntu-latest={RUNNER_IMAGE}",\n'
        '        "--platform",\n        "ubuntu-24.04=node:16-bullseye-slim",\n',
    ),
    # The accepted label set is dev's: ubuntu-latest only.
    "drop-2404-from-accepted-labels": (
        'RUNS_ON_LABELS = ("ubuntu-latest", "ubuntu-24.04")\n',
        'RUNS_ON_LABELS = ("ubuntu-latest",)\n',
    ),
    # The sandbox accepts any ubuntu- label.
    "accept-any-ubuntu-label": (
        "            if runs_on not in RUNS_ON_LABELS:\n",
        '            if not (isinstance(runs_on, str) and runs_on.startswith("ubuntu-")):\n',
    ),
    # The refusal stops naming the refused label (dev's wording).
    "refusal-omits-label": (
        '                    f"workflow {relative} job {job_id} runs on {runs_on!r}; only the "\n'
        '                    f"literal labels {\', \'.join(RUNS_ON_LABELS)} are replayed"\n',
        '                    f"workflow {relative} job {job_id} must use literal ubuntu-latest"\n',
    ),
}


def run(checkout: pathlib.Path, receipts: pathlib.Path, name: str) -> dict:
    """Plant `name`, run the isolated self-test, and return its receipt."""
    old, new = MUTANTS[name]
    source = (checkout / "scripts/act_ci.py").read_text(encoding="utf-8")
    if source.count(old) != 1:
        raise SystemExit(f"{name}: anchor occurs {source.count(old)} times")
    with tempfile.TemporaryDirectory(prefix="a673-mutant-") as raw:
        copy = pathlib.Path(raw) / "act_ci.py"
        copy.write_text(source.replace(old, new), encoding="utf-8")
        copy.chmod(0o555)
        result = subprocess.run(
            [sys.executable, "-I", str(copy), "--selftest", "--worktree", str(checkout)],
            cwd=raw, capture_output=True, text=True, check=False,
        )
        output = (result.stdout + result.stderr).replace(raw, "<copy>").replace(str(checkout), "<checkout>")
    fails = [line.strip() for line in output.splitlines() if line.startswith("  FAIL")]
    summary = [line for line in output.splitlines() if line.startswith("selftest:")]
    receipt = {"mutant": name, "replaced": old, "with": new, "returncode": result.returncode,
               "summary": summary, "fail_lines": fails}
    (receipts / f"mutant-{name}.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return receipt


def main() -> int:
    """Run every named mutant in order and print its verdict."""
    checkout, receipts = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2])
    for name in sys.argv[3:]:
        receipt = run(checkout, receipts, name)
        print(f"{name}: rc={receipt['returncode']} {receipt['summary']}")
        for line in receipt["fail_lines"]:
            print("   ", line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
