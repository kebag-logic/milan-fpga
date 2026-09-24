#!/usr/bin/env python3
"""[A220] Slot mutants of scripts/act_ci.py: the published A213 set, verbatim, plus A220's.

The A213 list is imported unchanged from its published script (532-review-evidence,
review-evidence/532-r1/correction-a213/bin/slot-mutants.py). Each mutant is one
exact substitution that must apply exactly once to the lane's act_ci.py; the
mutated text is written to a scratch file and bound READ-ONLY over
/work/scripts/act_ci.py inside run-selftest-sandbox.sh's network-less,
unprivileged sandbox, which binds the lane tree read-only. The lane file is
only read. KILLED means the self-test failed (or timed out); SURVIVED means it
passed.

Usage: slot-mutants-a220.py A213_SLOT_MUTANTS_PY LANE SANDBOX_SCRIPT SCRATCH user|root
"""

import hashlib
import importlib.util
import pathlib
import subprocess
import sys

A220_MUTANTS = [
    ("A220 missing max count read as zero",
     '        hits = int(events["max"])\n', '        hits = int(events.get("max", 0))\n'),
    ("A220 cap hits reported from the oom count",
     'the cap was hit {hits} "', 'the cap was hit {exhausted} "'),
    ("A220 a slice sitting at its cap without an OOM is refused too",
     "    if exhausted:\n", "    if exhausted or hits > 1000:\n"),
]


def main() -> int:
    """Apply each mutant to a scratch copy, run the sandboxed self-test, print one verdict line."""
    spec = importlib.util.spec_from_file_location("a213_slot_mutants", sys.argv[1])
    a213 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(a213)
    lane = pathlib.Path(sys.argv[2]).resolve()
    sandbox = pathlib.Path(sys.argv[3]).resolve()
    scratch = pathlib.Path(sys.argv[4]).resolve()
    as_uid = sys.argv[5]
    runner = lane / "scripts/act_ci.py"
    original = runner.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    text = original.decode("utf-8")
    scratch.mkdir(parents=True, exist_ok=True)
    mutated = scratch / "act_ci.py"
    print(f"lane act_ci.py sha256={digest} as={as_uid} mutants={len(a213.MUTANTS)}+{len(A220_MUTANTS)}",
          flush=True)
    for label, before, after in list(a213.MUTANTS) + A220_MUTANTS:
        count = text.count(before)
        if count != 1:
            print(f"{label}: NOT APPLIED (fragment occurs {count} times)", flush=True)
            continue
        mutated.write_text(text.replace(before, after, 1), encoding="utf-8")
        try:
            result = subprocess.run([str(sandbox), str(lane), as_uid, str(mutated)],
                                    capture_output=True, text=True, timeout=300, check=False)
            status, output = result.returncode, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            status, output = 124, "timed out"
        failed = [line.strip() for line in output.splitlines() if line.startswith("  FAIL")]
        print(f"{label}: {'KILLED' if status else 'SURVIVED'} rc={status}", flush=True)
        for line in failed[:3]:
            print(f"    {line[:220]}", flush=True)
        if status not in (0, 1) and not failed:
            for line in [line for line in output.splitlines() if line.strip()][-2:]:
                print(f"    | {line[:200]}", flush=True)
    mutated.unlink(missing_ok=True)
    after = hashlib.sha256(runner.read_bytes()).hexdigest()
    print(f"lane file after run sha256={after} {'EXACT' if after == digest else 'CHANGED'}")
    return 0 if after == digest else 2


if __name__ == "__main__":
    raise SystemExit(main())
