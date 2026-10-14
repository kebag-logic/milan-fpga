#!/usr/bin/env python3
"""Apply one textual mutation at a time to a disposable copy, run the named
selftest, restore the file, and record whether the selftest failed (killed).
Usage: python3 -I selftest_mutations.py <disposable-copy>"""
import json, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1])
M = [
 ("scripts/ci_case_receipts.py", "    if Counter(seen) != Counter(names):\n", "    if False:\n", "scripts/ci_case_receipts_selftest.py"),
 ("scripts/ci_case_receipts.py", "        if ran != selected:\n", "        if False:\n", "scripts/ci_case_receipts_selftest.py"),
 ("scripts/ci_case_receipts.py", "                if observations[name] != original[name]:\n", "                if False:\n", "scripts/ci_case_receipts_selftest.py"),
 ("scripts/ci_gate_receipts.py", "        if not isinstance(needs[job], dict) or needs[job].get(\"result\") != \"success\":\n", "        if False:\n", "scripts/ci_gate_workflows_selftest.py"),
 ("scripts/ci_gate_receipts.py", "    if len(scopes) != 1 or sorted(seen) != sorted(inventory) or len(set(seen)) != len(seen):\n", "    if False:\n", "scripts/ci_gate_workflows_selftest.py"),
 ("scripts/ci_fail_fast.py", "                   if job.get(\"conclusion\") in (\"failure\", \"cancelled\", \"timed_out\", \"action_required\")), None)\n", "                   if job.get(\"conclusion\") in (\"failure\",)), None)\n", "scripts/ci_fail_fast_selftest.py"),
 ("scripts/ci_fail_fast.py", "    complete = set(names) == expected and all(job[\"status\"] == \"completed\" for job in relevant)\n", "    complete = all(job[\"status\"] == \"completed\" for job in relevant)\n", "scripts/ci_fail_fast_selftest.py"),
 ("scripts/ci_manifest.py", "            if observed[\"outcome\"] != \"success\" or observed[\"skip_reason\"] is not None:\n", "            if False:\n", "scripts/ci_manifest_selftest.py"),
 ("scripts/suite_shards.py", "                 for worker, value in enumerate(load[:-len(DEDICATED_SUITES)]) if value > 1620]\n", "                 for worker, value in enumerate(load[:-len(DEDICATED_SUITES)]) if value > 99999]\n", "scripts/suite_shards.py --selftest"),
]
rows = []
for path, old, new, test in M:
    f = root / path; text = f.read_text()
    if text.count(old) != 1:
        rows.append({"file": path, "mutation": new.strip(), "status": "PATTERN-NOT-UNIQUE"}); continue
    f.write_text(text.replace(old, new))
    try:
        r = subprocess.run([sys.executable, *test.split()], cwd=root, capture_output=True, text=True, timeout=600,
                           env={"PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1", "HOME": str(root), "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid", "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@example.invalid"})
        rows.append({"file": path, "mutation": old.strip()[:90] + " -> " + new.strip()[:40], "selftest": test,
                     "rc": r.returncode, "killed": r.returncode != 0, "tail": (r.stdout + r.stderr).strip().splitlines()[-1:]})
    finally:
        f.write_text(text)
print(json.dumps(rows, indent=1))
