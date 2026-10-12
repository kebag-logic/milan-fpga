"""Order mutants for lane 730 round 4, adapted from R632-3 mutants_r3.py (MUTANTS list only): each mutant must fail the runner's self-test.

Usage: python3 -I mutants_r3.py <packet-dir> <pristine-tree> [--jobs N]

For each mutant: hard-link copy <pristine-tree> to <packet>/scratch/mut3/<id>,
replace scripts/act_ci.py with the mutated text (the anchor must occur exactly
once), then run `act_ci.py --selftest` through <packet>/scripts/sandbox.sh (no
network, no Docker socket). Prints one line per mutant with every failing arm,
and a tally. A SURVIVED mutant names behaviour no self-test arm pins.
"""

from __future__ import annotations

import concurrent.futures
import os
import pathlib
import shutil
import subprocess
import sys

PACKET = pathlib.Path(sys.argv[1]).resolve()
PRISTINE = pathlib.Path(sys.argv[2]).resolve()
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
SANDBOX = PACKET / "scripts" / "sandbox.sh"

MUTANTS: list[tuple[str, str, str, str]] = [
    ("O01", "the first selected workflow's concurrency wins",
     "        most = max(most, sum(widths[:CONCURRENT_JOB_LIMIT]))",
     "        most = most or sum(widths[:CONCURRENT_JOB_LIMIT])"),
    ("O02", "the selected workflows' concurrencies are added up",
     "        most = max(most, sum(widths[:CONCURRENT_JOB_LIMIT]))",
     "        most = most + sum(widths[:CONCURRENT_JOB_LIMIT])"),
    ("O03", "the least of the selected workflows wins",
     "        most = max(most, sum(widths[:CONCURRENT_JOB_LIMIT]))",
     "        most = min(most, sum(widths[:CONCURRENT_JOB_LIMIT])) if most else sum(widths[:CONCURRENT_JOB_LIMIT])"),
    ("O04", "only the first two selected workflows are read",
     "    most = 0\n    for workflow in workflows:\n        relative = WORKFLOWS[workflow]",
     "    most = 0\n    for workflow in workflows[:2]:\n        relative = WORKFLOWS[workflow]"),
    ("O05", "only the last two selected workflows are read",
     "    most = 0\n    for workflow in workflows:\n        relative = WORKFLOWS[workflow]",
     "    most = 0\n    for workflow in workflows[-2:]:\n        relative = WORKFLOWS[workflow]"),
    ("O06", "the last selected workflow wins (R632-3 Q24)",
     "        most = max(most, sum(widths[:CONCURRENT_JOB_LIMIT]))",
     "        most = sum(widths[:CONCURRENT_JOB_LIMIT])"),
]


def run_one(mutant: tuple[str, str, str, str]) -> str:
    ident, what, old, new = mutant
    tree = PACKET / "scratch" / "mut4" / ident
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(PRISTINE, tree, copy_function=os.link)
    target = tree / "scripts" / "act_ci.py"
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        shutil.rmtree(tree)
        return f"{ident} ANCHOR x{count} - {what}"
    target.unlink()
    target.write_text(text.replace(old, new), encoding="utf-8")
    result = subprocess.run(
        [str(SANDBOX), str(tree), "python3", "-I", "scripts/act_ci.py", "--selftest"],
        capture_output=True, text=True, timeout=900,
    )
    fails = [line.strip() for line in result.stdout.splitlines() if line.startswith("  FAIL")]
    verdict = "KILLED" if result.returncode != 0 else "SURVIVED"
    line = f"{ident} {verdict} rc={result.returncode} fails={len(fails)} - {what}"
    for each in fails:
        line += f"\n    {each[:220]}"
    if not fails and result.returncode != 0:
        line += f"\n    tail: {(result.stdout + result.stderr).strip().splitlines()[-1][:220]}"
    shutil.rmtree(tree)
    return line


def main() -> int:
    with concurrent.futures.ThreadPoolExecutor(JOBS) as pool:
        results = list(pool.map(run_one, MUTANTS))
    for line in results:
        print(line)
    killed = sum(1 for line in results if " KILLED " in line)
    survived = [line.split()[0] for line in results if " SURVIVED " in line]
    anchors = [line.split()[0] for line in results if " ANCHOR " in line]
    print(f"mutants: {len(results)}, killed {killed}, survived {survived}, bad anchors {anchors}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
