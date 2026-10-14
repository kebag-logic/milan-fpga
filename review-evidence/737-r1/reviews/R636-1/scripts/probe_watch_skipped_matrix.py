#!/usr/bin/env python3
"""Probe: feed the production fail-fast observer the job list GitHub returns
when rtl-full's scope gate skips its matrix jobs (shape copied from hosted run
38273578232), using the head's generated EXPECTED_JOBS. Usage:
  python3 -I probe_watch_skipped_matrix.py <clone-root> <hosted-jobs.json>
"""
import json, sys
from pathlib import Path
root = Path(sys.argv[1])
sys.path.insert(0, str(root / "scripts"))
import yaml
from ci_fail_fast import observe
wf = yaml.safe_load((root / ".github/workflows/rtl.yml").read_text())
step = [s for s in wf["jobs"]["ci-fail-fast"]["steps"] if s.get("name") == "Observe the first failed job"][0]
expected = set(json.loads(step["env"]["EXPECTED_JOBS"]))
hosted = json.loads(Path(sys.argv[2]).read_text())["jobs"]
# Hosted names for the skipped run, plus the head's new non-matrix jobs, all skipped.
jobs = [dict(j) for j in hosted]
for name in sorted(expected):
    if name.startswith("Union "):
        jobs.append({"name": name, "status": "completed", "conclusion": "skipped"})
complete, failed = observe(jobs, expected)
missing = sorted(expected - {j["name"] for j in jobs})
print(json.dumps({"complete": complete, "failed": failed, "missing_expected": missing,
                  "watcher_timeout_minutes": wf["jobs"]["ci-fail-fast"]["timeout-minutes"],
                  "manifest_needs_watcher": "ci-fail-fast" in wf["jobs"]["ci-manifest"]["needs"]}, indent=1))
sys.exit(0 if not complete and failed is None else 2)
