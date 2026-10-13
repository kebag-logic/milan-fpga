#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Execute the shipping scope steps on divergent histories and planted defects."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import textwrap


def git(root: Path, *args: str) -> str:
    """Run Git only in the disposable fixture, with no external hooks."""
    return subprocess.check_output(
        ["git", "-c", "core.hooksPath=/dev/null", "-c", "user.name=Scope fixture",
         "-c", "user.email=scope@example.invalid", "-C", str(root), *args],
        text=True, stderr=subprocess.STDOUT,
    ).strip()


def commit_file(root: Path, parent: str, path: str, text: str) -> str:
    """Commit one independent change from parent."""
    git(root, "checkout", "--quiet", "--detach", parent)
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    git(root, "add", path)
    git(root, "commit", "--quiet", "-m", "Scope control")
    return git(root, "rev-parse", "HEAD")


def history(root: Path, shipping: Path) -> tuple[str, str, list[tuple[str, str, list[str], str]]]:
    """A fork, two newer base commits, and four PR deltas with independent oracles."""
    git(root, "init", "--quiet")
    (root / "scripts").mkdir()
    shutil.copyfile(shipping / "scripts/ci_scope.py", root / "scripts/ci_scope.py")
    # A documentation-shaped gitlink makes removing the explicit pointer rule observable.
    (root / ".gitmodules").write_text(
        '[submodule "pointer"]\n\tpath = docs/pointer.md\n'
        '\turl = https://example.invalid/pointer.git\n', encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "--quiet", "-m", "Initial scope fixture")
    pointer = git(root, "rev-parse", "HEAD")
    git(root, "update-index", "--add", "--cacheinfo", f"160000,{pointer},docs/pointer.md")
    git(root, "commit", "--quiet", "-m", "Pointer baseline")
    common = git(root, "rev-parse", "HEAD")
    recorded = commit_file(root, common, "scripts/base.py", "base = 1\n")
    live = commit_file(root, recorded, "hdl/base.sv", "// base change\n")
    docs = commit_file(root, common, "docs/note.md", "PR documentation\n")
    rtl = commit_file(root, common, "hdl/pr.sv", "// PR change\n")
    git(root, "checkout", "--quiet", "--detach", common)
    git(root, "update-index", "--cacheinfo", f"160000,{recorded},docs/pointer.md")
    git(root, "commit", "--quiet", "-m", "Pointer control")
    moved = git(root, "rev-parse", "HEAD")
    return recorded, live, [
        ("stale-base docs", docs, ["docs/note.md"], "false"),
        ("stale-base RTL", rtl, ["hdl/pr.sv"], "true"),
        ("submodule pointer", moved, ["docs/pointer.md"], "true"),
        ("empty delta", common, [], "true"),
    ]


def scope_script(shipping: Path, workflow: str, job: str, step_id: str) -> str:
    """Read the actual workflow body, omitting only its recursive selftest call."""
    # Scope runs before dependency installation; the fixture needs only the
    # literal block shape independently pinned by ci_events.py.
    text = (shipping / ".github/workflows" / workflow).read_text()
    _, found, tail = text.partition(f"  {job}:\n")
    assert found, f"missing scope job: {workflow}"
    _, found, tail = tail.partition(f"        id: {step_id}\n")
    assert found, f"missing scope step: {workflow}"
    _, found, tail = tail.partition("        run: |\n")
    assert found, f"missing scope script: {workflow}"
    lines = []
    for line in tail.splitlines():
        if line.strip() and not line.startswith("          "):
            break
        lines.append(line)
    script = textwrap.dedent("\n".join(lines))
    proof = "python3 scripts/ci_scope.py --selftest"
    assert script.count(proof) == 1, "scope selftest wiring changed"
    return script.replace(proof, ":")


def execute(root: Path, script: str, recorded: str, head: str,
            checked_out: str, event: str = "pull_request") -> tuple[list[str], str]:
    """Execute one shipping scope body and read both its paths and output."""
    with tempfile.TemporaryDirectory(prefix="scope-output-") as raw:
        work = Path(raw)
        output = work / "output"
        env = dict(os.environ, EVENT_NAME=event, PR_BASE_SHA=recorded,
                   PR_HEAD_SHA=head, GITHUB_SHA=checked_out, PR_DRAFT="false",
                   PUSH_BEFORE_SHA=recorded, GITHUB_OUTPUT=str(output), RUNNER_TEMP=raw)
        # Use the interpreter running the gate for the workflow's python3.
        (work / "python3").symlink_to(sys.executable)
        env["PATH"] = raw + os.pathsep + env["PATH"]
        subprocess.run(["bash", "-euo", "pipefail", "-c", script], cwd=root,
                       env=env, check=True, capture_output=True, text=True)
        changed = next(work.glob("changed*"))
        verdicts = dict(line.split("=", 1) for line in output.read_text().splitlines())
        return changed.read_text().splitlines(), verdicts["rtl"]


def selftest(shipping: Path) -> int:
    """Every control must pass, then fail for its corresponding removed rule."""
    failures = 0

    def check(label: str, ok: bool) -> None:
        """Count a failed history assertion and print its independent oracle."""
        nonlocal failures
        print(f"  {'ok  ' if ok else 'FAIL'} scope history: {label}")
        failures += not ok

    with tempfile.TemporaryDirectory(prefix="ci-scope-history-") as raw:
        root = Path(raw)
        recorded, live, cases = history(root, shipping)
        for workflow, job, step in (
                ("rtl.yml", "full-ci-gate", "gate"),
                ("rtl-fast.yml", "changes", "scope"),
                ("elaborate.yml", "elaborate", "scope")):
            script = scope_script(shipping, workflow, job, step)
            for label, head, expected, verdict in cases:
                git(root, "checkout", "--quiet", "--detach", live)
                git(root, "merge", "--quiet", "--no-edit", head)
                merge = git(root, "rev-parse", "HEAD")
                hosted = execute(root, script, recorded, head, merge)
                git(root, "checkout", "--quiet", "--detach", head)
                replay = execute(root, script, recorded, head, head)
                check(f"{workflow} {label}: hosted = replay = {expected}, rtl={verdict}",
                      hosted == replay == (expected, verdict))
                classifier = root / "scripts/ci_scope.py"
                pristine = classifier.read_text()
                if verdict == "false":
                    mutant = script.replace("...$PR_HEAD_SHA", '" "$PR_HEAD_SHA')
                    check(f"{workflow} endpoint-tree mutation rejected",
                          execute(root, mutant, recorded, head, head) != (expected, verdict))
                    mutant = script.replace("$PR_HEAD_SHA", "$GITHUB_SHA")
                    check(f"{workflow} merge-commit scope mutation rejected",
                          execute(root, mutant, recorded, head, merge) != (expected, verdict))
                else:
                    old, new = {
                        "stale-base RTL": ('DOC_PREFIXES = ["LICENSES/"]',
                                           'DOC_PREFIXES = ["LICENSES/", "hdl/"]'),
                        "submodule pointer": ("is_submodule_path(clean) or ", ""),
                        "empty delta": ("not changed or ", ""),
                    }[label]
                    assert pristine.count(old) == 1, f"mutation anchor drift: {label}"
                    try:
                        classifier.write_text(pristine.replace(old, new))
                        check(f"{workflow} {label} rule-removal mutation rejected",
                              execute(root, script, recorded, head, head) != (expected, verdict))
                    finally:
                        classifier.write_text(pristine)
            if workflow == "rtl-fast.yml":
                # A push keeps its before-to-after tree comparison, even for a rewind.
                expected = ["hdl/base.sv"]
                check("fast push retains before-to-after comparison",
                      execute(root, script, live, recorded, recorded, "push")
                      == (expected, "true"))
    return int(failures)
