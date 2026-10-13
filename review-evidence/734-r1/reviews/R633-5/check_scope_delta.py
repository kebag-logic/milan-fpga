#!/usr/bin/env python3
"""Compare selector bodies and independently execute historical B16 objects."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import yaml

PREVIOUS = "59354ffe75697e17a16fd117d9ba853e104394bc"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    root, packet = args.root.resolve(), args.packet.resolve()
    scratch = packet / "scratch" / "b16"
    scratch.mkdir(parents=True, exist_ok=True)
    fixture = scratch / "repo"
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_NO_REPLACE_OBJECTS="1", GIT_OPTIONAL_LOCKS="0", PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(scratch))
    def git(where, *args):
        return subprocess.check_output(["git", "-c", "core.hooksPath=/dev/null", "-c", "maintenance.auto=false", "-c", "gc.auto=0", "-C", str(where), *args], env=env, stderr=subprocess.PIPE).decode().strip()
    git(root, "clone", "--shared", "--no-checkout", str(root), str(fixture))
    head = git(root, "rev-parse", "f1b2489f")
    merge = git(root, "rev-parse", "6c810c45")
    live = git(root, "rev-parse", f"{merge}^1")
    recorded = git(root, "rev-parse", "49da9fd9")
    paths = ["docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md", "docs/findings/README.md"]
    results = []
    for workflow, job, step_id in [("rtl.yml", "full-ci-gate", "gate"), ("rtl-fast.yml", "changes", "scope"), ("elaborate.yml", "elaborate", "scope")]:
        path = ".github/workflows/" + workflow
        current = (root / path).read_text()
        previous = git(root, "show", f"{PREVIOUS}:{path}")
        def step(text):
            return next(s for s in yaml.safe_load(text)["jobs"][job]["steps"] if s.get("id") == step_id)
        assert step(current) == step(previous), workflow
        script = step(current)["run"]
        assert script.count("python3 scripts/ci_scope.py --selftest") == 1
        script = script.replace("python3 scripts/ci_scope.py --selftest", ":")
        for replay in [False, True]:
            git(fixture, "checkout", "--quiet", "--force", "--detach", head if replay else merge)
            git(fixture, "update-ref", "refs/remotes/origin/dev", live)
            (fixture / "scripts/ci_scope.py").write_bytes((root / "scripts/ci_scope.py").read_bytes())
            case_dir = scratch / f"{workflow}-{replay}"
            case_dir.mkdir()
            output = case_dir / "output"
            case_env = dict(env, ACT="true" if replay else "false", EVENT_NAME="pull_request", PR_BASE_SHA=recorded, PR_BASE_REF="dev", PR_HEAD_SHA=head, GITHUB_SHA=head if replay else merge, PR_DRAFT="false", PUSH_BEFORE_SHA=recorded, GITHUB_OUTPUT=str(output), RUNNER_TEMP=str(case_dir))
            result = subprocess.run(["bash", "-euo", "pipefail", "-c", script], cwd=fixture, env=case_env, capture_output=True, text=True, timeout=30)
            changed = next(case_dir.glob("changed*"))
            observed = changed.read_text().splitlines()
            outputs = dict(line.split("=", 1) for line in output.read_text().splitlines())
            assert result.returncode == 0 and observed == paths and outputs["rtl"] == "false", (workflow, replay, result.stderr, observed, outputs)
            results.append({"workflow": workflow, "mode": "replay" if replay else "hosted", "returncode": result.returncode, "paths": observed, "outputs": outputs, "selector_step_identical_to_previous": True, "shell_sha256": hashlib.sha256(script.encode()).hexdigest(), "stdout": result.stdout, "stderr": result.stderr})
    outcome = {"reviewed_head": git(root, "rev-parse", "HEAD"), "historical_head": head, "historical_merge": merge, "historical_live": live, "historical_recorded": recorded, "results": results}
    (packet / "b16-scope-delta.json").write_text(json.dumps(outcome, indent=2) + "\n")
    print("PASS: three selector steps identical to previous head; all six real-object B16 executions retain two documentation paths and rtl=false")


if __name__ == "__main__":
    main()
