#!/usr/bin/env python3
"""Independent scope probes using YAML-decoded shipping shell bodies and real Git."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import yaml

p = argparse.ArgumentParser()
p.add_argument("source", type=Path)
p.add_argument("scratch", type=Path)
a = p.parse_args()
source = a.source.resolve()
a.scratch.mkdir(parents=True, exist_ok=True)
os.environ["TMPDIR"] = str(a.scratch.resolve())
tempfile.tempdir = str(a.scratch.resolve())
os.environ["GIT_CONFIG_GLOBAL"] = "/dev/null"
os.environ["GIT_CONFIG_NOSYSTEM"] = "1"
os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

def git(root, *args):
    return subprocess.check_output(
        ["git", "-c", "core.hooksPath=/dev/null", "-c", "user.name=Review fixture",
         "-c", "user.email=review@example.invalid", "-C", str(root), *args],
        text=True, stderr=subprocess.STDOUT).strip()

scopes = {}
for name, job, step in [("rtl.yml", "full-ci-gate", "gate"),
                        ("rtl-fast.yml", "changes", "scope"),
                        ("elaborate.yml", "elaborate", "scope")]:
    body = yaml.safe_load((source / ".github/workflows" / name).read_text())
    steps = body["jobs"][job]["steps"]
    assert steps[0]["with"]["fetch-depth"] == 0
    select = next(s for s in steps if s.get("id") == step)
    assert select["env"]["PR_HEAD_SHA"] == "${{ github.event.pull_request.head.sha }}"
    assert select["env"]["PR_BASE_SHA"] == "${{ github.event.pull_request.base.sha }}"
    assert select["run"].count("python3 scripts/ci_scope.py --selftest") == 1
    scopes[name] = select["run"].replace("python3 scripts/ci_scope.py --selftest", ":")

results = []
def check(root, label, base, head, checkout, expected_paths, expected_rtl,
          event="pull_request", draft="false", fails=False, workflow=None):
    for name, script in scopes.items():
        if workflow and name != workflow:
            continue
        with tempfile.TemporaryDirectory() as raw:
            d = Path(raw)
            env = dict(os.environ, EVENT_NAME=event, PR_BASE_SHA=base, PR_HEAD_SHA=head,
                       GITHUB_SHA=checkout, PUSH_BEFORE_SHA=base, PR_DRAFT=draft,
                       GITHUB_OUTPUT=str(d/"out"), RUNNER_TEMP=raw)
            r = subprocess.run(["bash", "-euo", "pipefail", "-c", script], cwd=root,
                               env=env, text=True, capture_output=True)
            values = dict(line.split("=", 1) for line in (d/"out").read_text().splitlines()) if (d/"out").exists() else {}
            changed = list(d.glob("changed*"))
            paths = changed[0].read_text().splitlines() if changed else None
            ok = (r.returncode != 0 and values.get("rtl") != "false") if fails else (
                r.returncode == 0 and values.get("rtl") == expected_rtl
                and (expected_paths is None or paths == expected_paths))
            if not fails and name == "rtl.yml":
                full = event != "pull_request" or (draft == "false" and expected_rtl == "true")
                ok = ok and values.get("run_full") == str(full).lower()
            row = dict(case=label, workflow=name, rc=r.returncode, paths=paths,
                       outputs=values, pass_check=ok)
            if r.returncode: row["stderr"] = r.stderr.strip()
            print(json.dumps(row), flush=True)
            results.append(row)
            assert ok, row

# Real B16 commits: default rename detection yields 64 paths; shipping --no-renames yields 65.
b16_base = git(source, "rev-parse", "49da9fd9")
b16_head = git(source, "rev-parse", "f1b2489f")
for flags, count in [([], 64), (["--no-renames"], 65)]:
    paths = git(source, "diff", *flags, "--name-only", b16_base, b16_head).splitlines()
    assert len(paths) == count
    print(json.dumps(dict(case="B16 endpoint", flags=flags, count=count, paths=paths)))
expected = ["docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md", "docs/findings/README.md"]
assert git(source, "diff", "--no-renames", "--name-only", b16_base+"..."+b16_head).splitlines() == expected
check(source, "B16 replay SHA", b16_base, b16_head, b16_head, expected, "false")
check(source, "B16 unrelated checkout SHA cannot affect scope", b16_base, b16_head,
      git(source, "rev-parse", "HEAD"), expected, "false")

with tempfile.TemporaryDirectory() as raw:
    root = Path(raw)
    git(root, "init", "--quiet")
    (root/"scripts").mkdir()
    shutil.copyfile(source/"scripts/ci_scope.py", root/"scripts/ci_scope.py")
    (root/"hdl").mkdir()
    (root/"hdl/original.sv").write_text("module original; endmodule\n")
    git(root, "add", "."); git(root, "commit", "-qm", "Common")
    common = git(root, "rev-parse", "HEAD")
    (root/"hdl/base.sv").write_text("module base; endmodule\n")
    git(root, "add", "."); git(root, "commit", "-qm", "Base moved")
    base = git(root, "rev-parse", "HEAD")
    git(root, "checkout", "--detach", "--quiet", common)
    (root/"docs").mkdir()
    (root/"docs/note.md").write_text("A documentation change\n")
    git(root, "add", "."); git(root, "commit", "-qm", "Docs")
    docs = git(root, "rev-parse", "HEAD")
    check(root, "independent stale docs", base, docs, base, ["docs/note.md"], "false")
    check(root, "unknown base fallback", "f"*40, docs, docs, None, "true")
    check(root, "missing base fallback", "", docs, docs, None, "true")
    check(root, "invalid head fails closed", base, "e"*40, docs, None, None, fails=True)
    check(root, "empty PR fails safe", base, common, docs, [], "true")
    check(root, "push rewind", base, common, common, ["hdl/base.sv"], "true", event="push", workflow="rtl-fast.yml")
    check(root, "push docs", common, docs, docs, ["docs/note.md"], "false", event="push", workflow="rtl-fast.yml")
    for event in ("push", "schedule", "workflow_dispatch"):
        for wf in ("rtl.yml", "elaborate.yml"):
            check(root, "unconditional non-PR "+event, "", "", docs, None, "true", event=event, workflow=wf)
    (root/"hdl/new.sv").write_text("module pr; endmodule\n")
    git(root, "add", "."); git(root, "commit", "-qm", "Mixed")
    mixed = git(root, "rev-parse", "HEAD")
    check(root, "own RTL plus docs remains relevant", base, mixed, docs, ["docs/note.md", "hdl/new.sv"], "true")
    check(root, "draft RTL is relevant with exhaustive deferred", base, mixed, docs, ["docs/note.md", "hdl/new.sv"], "true", draft="true")
    git(root, "checkout", "--detach", "--quiet", common)
    (root/"docs").mkdir(exist_ok=True)
    git(root, "mv", "hdl/original.sv", "docs/renamed.md")
    git(root, "commit", "-qm", "Rename source to prose path")
    rename = git(root, "rev-parse", "HEAD")
    check(root, "RTL renamed to docs retains deletion", base, rename, base, ["docs/renamed.md", "hdl/original.sv"], "true")
    git(root, "checkout", "--detach", "--quiet", common)
    git(root, "rm", "hdl/original.sv"); git(root, "commit", "-qm", "Delete source")
    deletion = git(root, "rev-parse", "HEAD")
    check(root, "RTL deletion remains relevant", base, deletion, base, ["hdl/original.sv"], "true")
    tree = git(root, "rev-parse", "HEAD^{tree}")
    unrelated = git(root, "commit-tree", tree, "-m", "Unrelated root")
    check(root, "no merge base fails closed", base, unrelated, base, None, None, fails=True)
print(json.dumps(dict(result="PASS", shipping_scope_executions=len(results))))
