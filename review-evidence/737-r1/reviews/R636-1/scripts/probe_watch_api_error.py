#!/usr/bin/env python3
"""Probe: run the production watcher (`ci_fail_fast.py watch`) against an API
whose first jobs read returns HTTP 403 (rate limit) or a transient 502.
No network: urlopen is replaced. Usage:
  python3 -I probe_watch_api_error.py <clone-root> <scratch-dir>
"""
import json, os, sys
from pathlib import Path
from urllib.error import HTTPError
root, scratch = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(root / "scripts"))
import ci_fail_fast
scratch.mkdir(parents=True, exist_ok=True)
event = scratch / "event.json"
repo = "fixture/project"
event.write_text(json.dumps({"repository": {"full_name": repo},
                             "pull_request": {"head": {"repo": {"full_name": repo}, "sha": "a" * 40}}}))
os.environ.update(GITHUB_EVENT_PATH=str(event), GITHUB_REPOSITORY=repo, GITHUB_EVENT_NAME="pull_request",
                  GH_TOKEN="x", GITHUB_RUN_ID="1", EXPECTED_JOBS='["one"]')
os.environ.pop("ACT", None)
results = {}
for code in (403, 502):
    def fake(request, timeout=30, code=code):
        raise HTTPError(request.full_url, code, "fixture", {}, None)
    ci_fail_fast.urlopen = fake
    sys.argv = ["ci_fail_fast.py", "watch"]
    try:
        rc = ci_fail_fast.main()
        results[code] = {"returned": rc}
    except BaseException as exc:  # what the job step would see: non-zero exit
        results[code] = {"raised": type(exc).__name__, "step_outcome": "failure",
                         "next_step": "Cancel this run and sibling workflows (if: failure())"}
print(json.dumps(results, indent=1))
