#!/usr/bin/env python3
"""Plant one source mutation at a time in a disposable copy and require the
owning self-test to fail. Usage: mutation_probes.py <copy> <python> <out.json>
Each mutation is reverted (exact original bytes restored) before the next."""
import json, subprocess, sys
from pathlib import Path

copy, py, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
MUTANTS = [
    ("ff-drop-action_required", "scripts/ci_fail_fast.py",
     'FAILURES = ("failure", "cancelled", "timed_out", "action_required")',
     'FAILURES = ("failure", "cancelled", "timed_out")', ["scripts/ci_fail_fast_selftest.py"]),
    ("ff-observer-error-is-failure", "scripts/ci_fail_fast.py",
     'print("Observer unavailable: " + type(exc).__name__)\n        return 2',
     'print("Observer unavailable: " + type(exc).__name__)\n        return 1', ["scripts/ci_fail_fast_selftest.py"]),
    ("ff-5xx-not-transient", "scripts/ci_fail_fast.py",
     'or 500 <= exc.code < 600', 'or 500 <= exc.code < 501', ["scripts/ci_fail_fast_selftest.py"]),
    ("ff-skipped-raw-any-status", "scripts/ci_fail_fast.py",
     'if job.get("status") == "completed" and job.get("conclusion") == "skipped":',
     'if True:', ["scripts/ci_fail_fast_selftest.py"]),
    ("ff-tail-ignores-collector", "scripts/ci_fail_fast.py",
     'return any(row.get("result") in FAILURES and not (',
     'return any(job == "ci-fail-fast" and row.get("result") in FAILURES and not (', ["scripts/ci_fail_fast_selftest.py"]),
    ("ff-fork-allowed", "scripts/ci_fail_fast.py",
     '        and event.get("pull_request", {}).get("head", {}).get("repo", {}).get("full_name") == repository)',
     '        )', ["scripts/ci_fail_fast_selftest.py"]),
    ("shards-1620-to-1700", "scripts/suite_shards.py",
     'if value > 1620]', 'if value > 1700]', ["scripts/suite_shards.py", "--selftest"]),
    ("receipts-no-union-count", "scripts/ci_case_receipts.py",
     'if Counter(seen) != Counter(names):', 'if False:', ["scripts/ci_case_receipts_selftest.py"]),
    ("receipts-accept-failed", "scripts/ci_case_receipts.py",
     'outcome not in ("pass", "caught")', 'outcome not in ("pass", "caught", "failed")', ["scripts/ci_case_receipts_selftest.py"]),
    ("manifest-ignore-skip", "scripts/ci_manifest.py",
     'if observed["outcome"] != "success" or observed["skip_reason"] is not None:',
     'if observed["outcome"] not in ("success", "skipped"):', ["scripts/ci_manifest_selftest.py"]),
]
results = []
for name, rel, old, new, test in MUTANTS:
    path = copy / rel
    original = path.read_bytes()
    text = original.decode()
    if text.count(old) != 1:
        results.append({"mutant": name, "status": "ANCHOR NOT UNIQUE", "count": text.count(old)})
        continue
    path.write_text(text.replace(old, new))
    try:
        run = subprocess.run([py, *test], cwd=copy, capture_output=True, text=True, timeout=500)
        rc = run.returncode
        tail = (run.stdout + run.stderr).strip().splitlines()[-2:]
    except subprocess.TimeoutExpired:
        rc, tail = "timeout", []
    finally:
        path.write_bytes(original)
    results.append({"mutant": name, "file": rel, "test": test, "rc": rc,
                    "caught": rc not in (0, "timeout"), "tail": tail})
out.write_text(json.dumps(results, indent=1) + "\n")
for row in results:
    print(row["mutant"], "CAUGHT" if row.get("caught") else "SURVIVED/" + str(row.get("status", row.get("rc"))))
