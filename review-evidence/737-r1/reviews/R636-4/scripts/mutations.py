#!/usr/bin/env python3
"""Disposable mutation probes for PR #739 round 4 (reviewer-owned).

Usage: python3 -I mutations.py <tree> <out-dir> [mutant ...]

Each mutant edits tracked files in <tree> by exact string replacement (the
original text must occur exactly once), runs its killing command, records the
return code and log, then restores the files with `git checkout --`.  A mutant
is KILLED when the command returns non-zero.  "pristine" runs a command on the
unmodified tree and must return zero.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

SELF_GATE = ["python3", "scripts/ci_gate_workflows_selftest.py"]
SELF_FAIL = ["python3", "scripts/ci_fail_fast_selftest.py"]
SELF_RUNTIME = ["python3", "scripts/ci_runtime_evidence_selftest.py"]
EVENTS = ["python3", "scripts/ci_events.py", "--check"]

MUTANTS = {
    # R636-3-F1: the collector constructs its API without the shared read deadline.
    "i3-no-shared-budget": ([("scripts/ci_runtime_evidence.py",
                              'API(os.environ["GITHUB_REPOSITORY"], os.environ["GH_TOKEN"], RETRY_BUDGET_SECONDS)',
                              'API(os.environ["GITHUB_REPOSITORY"], os.environ["GH_TOKEN"])')], SELF_RUNTIME),
    # S1: a conditional or continue-on-error preparation is accepted.
    "i1-conditional-prep-accepted": ([("scripts/ci_suite_workflows.py",
                                       'body.strip() == preparation and "if" not in step and not step.get("continue-on-error")',
                                       'body.strip() == preparation')], SELF_GATE),
    "i1b-continue-on-error-accepted": ([("scripts/ci_suite_workflows.py",
                                         ' and not step.get("continue-on-error")', '')], SELF_GATE),
    # S2 watcher: a client error becomes observer-only.
    "s2-watcher-client-observer": ([("scripts/ci_fail_fast.py",
                                     "        if isinstance(exc, OSError) and not transient(exc):",
                                     "        if False:")], SELF_FAIL),
    # S2 collector: a client error becomes observer-only.
    "s2-collector-client-observer": ([("scripts/ci_runtime_evidence.py",
                                       "            if not transient(exc):\n                raise\n", "")], SELF_RUNTIME),
    # S2 classifier too broad: 404 counted transient.
    "s2-404-transient-watch": ([("scripts/ci_fail_fast.py",
                                 "error.code in (403, 429)", "error.code in (403, 404, 429)")], SELF_FAIL),
    "s2-404-transient-collect": ([("scripts/ci_fail_fast.py",
                                   "error.code in (403, 429)", "error.code in (403, 404, 429)")], SELF_RUNTIME),
    # S2 classifier too narrow: 429 counted genuine.
    "s2-429-genuine-watch": ([("scripts/ci_fail_fast.py",
                               "error.code in (403, 429)", "error.code in (403,)")], SELF_FAIL),
    "s2-429-genuine-collect": ([("scripts/ci_fail_fast.py",
                                 "error.code in (403, 429)", "error.code in (403,)")], SELF_RUNTIME),
    # S2: transport errors (URLError) counted genuine.
    "s2-transport-genuine-watch": ([("scripts/ci_fail_fast.py",
                                     "return not isinstance(error, HTTPError) or error.code",
                                     "return error.code")], SELF_FAIL),
    # S2: non-timeout transport errors (URLError) counted genuine, well-formed.
    "s2-urlerror-genuine-watch": ([("scripts/ci_fail_fast.py",
                                    "return not isinstance(error, HTTPError) or error.code in (403, 429) or 500 <= error.code < 600",
                                    "return isinstance(error, TimeoutError) or (isinstance(error, HTTPError) and "
                                    "(error.code in (403, 429) or 500 <= error.code < 600))"),
                                   ("scripts/ci_fail_fast.py", 'print(f"Watcher read refused: HTTP {exc.code}")',
                                    'print(f"Watcher read refused: HTTP {getattr(exc, \'code\', None)}")')],
                                  SELF_FAIL),
    "s2-urlerror-genuine-collect": ([("scripts/ci_fail_fast.py",
                                      "return not isinstance(error, HTTPError) or error.code in (403, 429) or 500 <= error.code < 600",
                                      "return isinstance(error, TimeoutError) or (isinstance(error, HTTPError) and "
                                      "(error.code in (403, 429) or 500 <= error.code < 600))"),
                                     ("scripts/ci_fail_fast.py", 'print(f"Watcher read refused: HTTP {exc.code}")',
                                      'print(f"Watcher read refused: HTTP {getattr(exc, \'code\', None)}")')],
                                    SELF_RUNTIME),
    # S3 union: a leg without the flag is accepted for the elaboration owners.
    "s3-unjudged-accepted": ([("scripts/ci_builder_legs.py",
                               'unjudged = [gate for gate in owners if gate in executed and flag not in executed[gate][1]]',
                               'unjudged = []')], SELF_GATE),
    # S3 union: an owner deleted from the inventory is accepted.
    "s3-absent-accepted": ([("scripts/ci_builder_legs.py",
                             'absent = [gate for gate in owners if gate not in names]', 'absent = []'),
                            ("scripts/ci_builder_legs.py",
                             'unrun = [gate for gate in owners if gate in names and gate not in executed]',
                             'unrun = [gate for gate in owners if gate in names and gate not in executed and False]')],
                           SELF_GATE),
    # S3 union: the driver's elaboration verdict is not applied to the union ledger.
    "s3-no-union-elaboration-verdict": ([("scripts/ci_builder_legs.py",
                                          "    if elaboration_verdict(ledger):",
                                          "    if False and elaboration_verdict(ledger):")], SELF_GATE),
    # S3 union: a leg's own failed elaboration verdict is accepted.
    "s3-leg-verdict-ignored": ([("scripts/ci_builder_legs.py",
                                 "    if driver[\"require_elaboration\"] != (0 if \"--require-elaboration\" in flags else None):",
                                 "    if False:")], SELF_GATE),
    # S3 union: a missing leg is accepted.
    "s3-missing-leg-accepted": ([("scripts/ci_builder_legs.py",
                                  "    if sorted(seen) != list(range(len(legs))):",
                                  "    if False:"),
                                 ("scripts/ci_builder_legs.py",
                                  'ledger = [tuple(item) for name in names for item in executed[name][0]["not_run"]]',
                                  'ledger = [tuple(item) for name in names if name in executed for item in executed[name][0]["not_run"]]'),
                                 ("scripts/ci_builder_legs.py",
                                  'observed = [executed[name][0] for name in names]',
                                  'observed = [executed[name][0] for name in names if name in executed]'),
                                 ("scripts/ci_builder_legs.py",
                                  'unrun = [gate for gate in owners if gate in names and gate not in executed]',
                                  'unrun = []')], SELF_GATE),
    # S3 compare: NOT RUN rows not compared with the unsharded reference.
    "s3-compare-ignores-not-run": ([("scripts/ci_builder_legs.py",
                                     '        if sharded[row["gate"]] != row:',
                                     '        if sharded[row["gate"]]["verdict"] != row["verdict"]:'),
                                    ("scripts/ci_builder_legs.py",
                                     '    if [item for row in rows for item in row["not_run"]] != result["not_run"]:',
                                     '    if False:')], SELF_GATE),
    # S3 aggregate: an executed division is accepted without builder receipts.
    "s3-aggregate-skips-union": ([("scripts/ci_gate_receipts.py",
                                   "    if any(divided):\n        from ci_builder_legs import union\n        union(builder or [], identity[0], identity[1])\n    elif builder:",
                                   "    if builder:")], SELF_GATE),
    # S3 aggregate, targeted: an executed division never consults the builder union.
    "s3-aggregate-no-union-call": ([("scripts/ci_gate_receipts.py",
                                     "        union(builder or [], identity[0], identity[1])\n    elif builder:",
                                     "        pass\n    elif builder:")], SELF_GATE),
    # S3 owners: one LiteX-consulting gate dropped from the named owners.
    "s3-owner-list-short": ([("scripts/ci_builder_legs.py",
                              '"test_toolchain_patch_gate_bites"),', '),')], SELF_GATE),
    # S3 generator: the leg step drops its selection (runs the full driver twice).
    "s3-generator-leg-wrong": ([("scripts/ci_gate_workflows.py",
                                 'kept["run"] = ("python3 scripts/ci_builder_legs.py run " + str(case["builder"])',
                                 'kept["run"] = ("python3 scripts/ci_builder_legs.py run all"')],
                               ["python3", "scripts/ci_gate_workflows.py", "--check"]),
    # S4: the field-oracle build loses its job bound.
    "s4-unbounded-field-oracle": ([(".github/workflows/rtl.yml",
                                    '--target packet_gen --parallel "$CI_TOOL_BUILD_JOBS"',
                                    "--target packet_gen --parallel"),
                                   (".github/ci-templates/rtl.yml",
                                    '--target packet_gen --parallel "$CI_TOOL_BUILD_JOBS"',
                                    "--target packet_gen --parallel")], EVENTS),
}

PRISTINE = {"pristine-gate": SELF_GATE, "pristine-fail": SELF_FAIL, "pristine-runtime": SELF_RUNTIME,
            "pristine-generator": ["python3", "scripts/ci_gate_workflows.py", "--check"]}


def run(tree: Path, out: Path, name: str) -> dict:
    """Apply, run, restore; return the record."""
    edits, command = MUTANTS[name] if name in MUTANTS else ([], PRISTINE[name])
    touched = sorted({path for path, _, _ in edits})
    for path, old, new in edits:
        target = tree / path
        text = target.read_text(encoding="utf-8")
        if text.count(old) != 1:
            raise SystemExit(f"{name}: anchor occurs {text.count(old)} times in {path}")
        target.write_text(text.replace(old, new), encoding="utf-8")
    start = time.monotonic()
    try:
        with (out / (name + ".log")).open("w", encoding="utf-8") as log:
            rc = subprocess.run(command, cwd=tree, stdout=log, stderr=subprocess.STDOUT,
                                check=False, timeout=1800).returncode
    finally:
        if touched:
            subprocess.run(["git", "checkout", "--", *touched], cwd=tree, check=True)
    clean = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=tree,
                           capture_output=True, text=True, check=True).stdout
    if clean:
        raise SystemExit(f"{name}: tree not restored: {clean}")
    record = {"name": name, "rc": rc, "seconds": round(time.monotonic() - start, 1),
              "expected": "rc 0" if name in PRISTINE else "non-zero",
              "verdict": ("PASS" if rc == 0 else "FAIL") if name in PRISTINE else ("KILLED" if rc else "SURVIVED"),
              "files": touched, "command": command}
    print(json.dumps(record), flush=True)
    return record


def main() -> int:
    tree, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    names = sys.argv[3:] or [*PRISTINE, *MUTANTS]
    records = [run(tree, out, name) for name in names]
    with (out / "summary.jsonl").open("a", encoding="utf-8") as stream:
        for record in records:
            stream.write(json.dumps(record) + "\n")
    bad = [r["name"] for r in records if r["verdict"] in ("SURVIVED", "FAIL")]
    print("bad:", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
