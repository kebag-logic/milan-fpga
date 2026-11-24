#!/usr/bin/env python3
"""Execute verilator-suites' generated preflight step, as committed in
.github/workflows/rtl.yml, over a real preflight output directory.

usage: python3 -I run_aggregate_step.py REPO RUNNER_TEMP RESULT

RUNNER_TEMP must contain suite-preflight/ as the job uploaded it. GITHUB_SHA
and the gate SHA are the repository's HEAD. Prints the step's exit status.
"""

import os
import subprocess
import sys
from pathlib import Path

import yaml


def main() -> int:
    repo, runner_temp, result = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3]
    workflow = yaml.safe_load((repo / ".github/workflows/rtl.yml").read_text())
    [step] = [s for s in workflow["jobs"]["verilator-suites"]["steps"]
              if s.get("name") == "Require the preflight to have passed for this run's SHA"]
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True,
                          check=True).stdout.strip()
    env = dict(os.environ, RUNNER_TEMP=runner_temp, GITHUB_SHA=head, GATE_SHA=head,
               PREFLIGHT_RESULT=result)
    ran = subprocess.run(["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", step["run"]],
                         cwd=repo, env=env, capture_output=True, text=True)
    sys.stdout.write(ran.stdout)
    sys.stdout.write(ran.stderr)
    print(f"verilator-suites preflight step with result={result}: exit {ran.returncode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
