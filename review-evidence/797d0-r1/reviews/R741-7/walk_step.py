#!/usr/bin/env python3
"""Walk named workflow steps alone through the image command-table walker.

Usage: CI_IMAGE_SHFMT=<pinned shfmt> python3 -E -s walk_step.py <repo-root> <workflow> <step-name>...
Imports the walker from <repo-root>/scripts, builds one Audit exactly as
ci_tool_inventory.derive() does, and runs each named step's `run:` text through
Audit.shell(); prints PASS or the refusal per step.  Exit 0 only if all pass.
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "scripts"))
import yaml  # noqa: E402
import ci_tool_inventory as inv  # noqa: E402
from ci_command_table import Audit, Refusal, Runtime  # noqa: E402

workflow = sys.argv[2]
names = sys.argv[3:]
doc = yaml.safe_load((root / workflow).read_bytes())
bad = 0
seen = set()
for job, body in doc["jobs"].items():
    for index, step in enumerate(body.get("steps", [])):
        if step.get("name") not in names:
            continue
        seen.add(step["name"])
        audit = Audit(root, {})
        audit.install_reader = inv.shell_installs
        env = {**doc.get("env", {}), **body.get("env", {}), **step.get("env", {})}
        audit.requests = []
        audit.env = {k: Runtime(v) if isinstance(v, str) and "${{" in v else str(v) for k, v in env.items()}
        audit.exported_env = dict(audit.env)
        try:
            audit.shell(step.get("run", ""), workflow, root, dialect="bash -e")
            print(f"PASS {workflow} job={job} step#{index} {step['name']!r} requests={audit.requests}")
        except Refusal as exc:
            bad += 1
            print(f"REFUSED {workflow} job={job} step#{index} {step['name']!r}: {exc}")
for n in names:
    if n not in seen:
        bad += 1
        print(f"NOT FOUND step {n!r}")
sys.exit(1 if bad else 0)
