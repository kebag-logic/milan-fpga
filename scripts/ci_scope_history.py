#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Execute the shipping scope steps on divergent histories and planted defects."""

from __future__ import annotations

from dataclasses import dataclass
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


@dataclass(frozen=True)
class ScopeCase:
    """A PR history with independent changed-path and relevance oracles."""

    label: str
    recorded: str
    live: str
    head: str
    paths: list[str]
    rtl: str


def history(root: Path, shipping: Path) -> list[ScopeCase]:
    """Forked PRs and lanes that merge newer dev, restore RTL, then edit docs."""
    git(root, "init", "--quiet")
    (root / "scripts").mkdir()
    shutil.copyfile(shipping / "scripts/ci_scope.py", root / "scripts/ci_scope.py")
    (root / "hdl").mkdir()
    (root / "hdl/x.sv").write_text("// original RTL\n", encoding="utf-8")
    # A documentation-shaped gitlink exposes removal of the explicit pointer rule.
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
    b16 = commit_file(root, docs, "docs/findings/README.md", "Finding index\n")
    rtl = commit_file(root, common, "hdl/pr.sv", "// PR change\n")
    git(root, "checkout", "--quiet", "--detach", common)
    git(root, "update-index", "--cacheinfo", f"160000,{recorded},docs/pointer.md")
    git(root, "commit", "--quiet", "-m", "Pointer control")
    moved = git(root, "rev-parse", "HEAD")
    newer = commit_file(root, common, "hdl/x.sv", "// newer dev RTL\n")
    git(root, "checkout", "--quiet", "--detach", docs)
    git(root, "merge", "--quiet", "--no-ff", "--no-edit", newer)
    restored = commit_file(root, git(root, "rev-parse", "HEAD"),
                           "hdl/x.sv", "// original RTL\n")
    restored = commit_file(root, restored, "docs/note.md", "Final PR documentation\n")
    later = commit_file(root, newer, "hdl/later.sv", "// unrelated dev RTL\n")
    return [
        ScopeCase("stale-base docs", recorded, live, docs, ["docs/note.md"], "false"),
        ScopeCase("B16 shape", recorded, live, b16,
                  ["docs/findings/README.md", "docs/note.md"], "false"),
        ScopeCase("stale-base RTL", recorded, live, rtl, ["hdl/pr.sv"], "true"),
        ScopeCase("submodule pointer", recorded, live, moved, ["docs/pointer.md"], "true"),
        ScopeCase("empty delta", recorded, live, common, [], "true"),
        ScopeCase("REV", common, newer, restored, ["docs/note.md", "hdl/x.sv"], "true"),
        ScopeCase("REV+E", common, later, restored, ["docs/note.md", "hdl/x.sv"], "true"),
    ]


def merge_checkout(root: Path, case: ScopeCase) -> str:
    """Build a synthetic merge with the live base as first parent, even for no delta."""
    git(root, "checkout", "--quiet", "--detach", case.live)
    git(root, "merge", "--quiet", "--no-ff", "--no-edit", case.head)
    merge = git(root, "rev-parse", "HEAD")
    if merge == case.live:
        merge = git(root, "commit-tree", f"{merge}^{{tree}}", "-p", case.live,
                    "-p", case.head, "-m", "Empty PR merge")
        git(root, "checkout", "--quiet", "--detach", merge)
    return merge


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
            checked_out: str, *, inputs: dict[str, str] | None = None) -> tuple[list[str], str]:
    """Execute one shipping scope body and read both its paths and output."""
    with tempfile.TemporaryDirectory(prefix="scope-output-") as raw:
        work = Path(raw)
        output = work / "output"
        env = dict(os.environ, ACT="false", EVENT_NAME="pull_request",
                   PR_BASE_SHA=recorded, PR_BASE_REF="dev",
                   PR_HEAD_SHA=head, GITHUB_SHA=checked_out, PR_DRAFT="false",
                   PUSH_BEFORE_SHA=recorded, GITHUB_OUTPUT=str(output), RUNNER_TEMP=raw)
        env.update(inputs or {})
        # Use the interpreter running the gate for the workflow's python3.
        (work / "python3").symlink_to(sys.executable)
        env["PATH"] = raw + os.pathsep + env["PATH"]
        subprocess.run(["bash", "-euo", "pipefail", "-c", script], cwd=root,
                       env=env, check=True, capture_output=True, text=True)
        changed = next(work.glob("changed*"))
        verdicts = dict(line.split("=", 1) for line in output.read_text().splitlines())
        return changed.read_text().splitlines(), verdicts["rtl"]


def refuses(root: Path, script: str, case: ScopeCase, checked_out: str,
            inputs: dict[str, str]) -> bool:
    """A failed shell step cannot release a documentation-only skip."""
    try:
        execute(root, script, case.recorded, case.head, checked_out, inputs=inputs)
    except subprocess.CalledProcessError:
        return True
    return False


def criss_cross(root: Path, parent: str) -> ScopeCase:
    """Two ordered merges have two merge bases, neither a unique scope authority."""
    left = commit_file(root, parent, "docs/left.md", "Left branch\n")
    right = commit_file(root, parent, "docs/right.md", "Right branch\n")
    first = merge_checkout(root, ScopeCase("left merge", parent, left, right, [], "true"))
    second = merge_checkout(root, ScopeCase("right merge", parent, right, left, [], "true"))
    assert len(git(root, "merge-base", "--all", first, second).splitlines()) == 2
    return ScopeCase("ambiguous base", parent, first, second, [], "true")


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
        cases = history(root, shipping)
        ambiguous = criss_cross(root, cases[4].head)
        for workflow, job, step in (
                ("rtl.yml", "full-ci-gate", "gate"),
                ("rtl-fast.yml", "changes", "scope"),
                ("elaborate.yml", "elaborate", "scope")):
            script = scope_script(shipping, workflow, job, step)
            for case in cases:
                merge = merge_checkout(root, case)
                hosted = execute(root, script, case.recorded, case.head, merge)
                git(root, "checkout", "--quiet", "--detach", case.head)
                git(root, "update-ref", "refs/remotes/origin/dev", case.live)
                replay = execute(root, script, case.recorded, case.head, case.head, inputs={"ACT": "true"})
                expected = (case.paths, case.rtl)
                check(f"{workflow} {case.label}: hosted = replay = {expected}",
                      hosted == replay == expected)
                # Both former frozen-base formulas must lose these real lane controls.
                if case.label in ("REV", "REV+E") or case.rtl == "false":
                    mutant = script.replace('"$GITHUB_SHA^1" "$GITHUB_SHA"',
                                            '"$PR_BASE_SHA" "$GITHUB_SHA"')
                    check(f"{workflow} {case.label} hosted frozen-base mutation rejected",
                          execute(root, mutant, case.recorded, case.head, merge) != expected)
                if case.label in ("REV", "REV+E"):
                    mutant = script.replace('"refs/remotes/origin/$PR_BASE_REF" "$PR_HEAD_SHA"',
                                            '"$PR_BASE_SHA" "$PR_HEAD_SHA"')
                    check(f"{workflow} {case.label} replay frozen-base mutation rejected",
                          execute(root, mutant, case.recorded, case.head, case.head,
                                  inputs={"ACT": "true"}) != expected)
                    mutant = script.replace('"$GITHUB_SHA^1" "$GITHUB_SHA"',
                                            '"$PR_BASE_SHA...$PR_HEAD_SHA"')
                    check(f"{workflow} {case.label} hosted frozen merge-base mutation rejected",
                          execute(root, mutant, case.recorded, case.head, merge) != expected)
                elif case.rtl == "false":
                    mutant = script.replace('"$base" "$PR_HEAD_SHA"',
                                            '"refs/remotes/origin/$PR_BASE_REF" "$PR_HEAD_SHA"')
                    check(f"{workflow} {case.label} replay endpoint mutation rejected",
                          execute(root, mutant, case.live, case.head, case.head,
                                  inputs={"ACT": "true"}) != expected)
                else:
                    classifier = root / "scripts/ci_scope.py"
                    pristine = classifier.read_text()
                    old, new = {
                        "stale-base RTL": ('DOC_PREFIXES = ["LICENSES/"]',
                                           'DOC_PREFIXES = ["LICENSES/", "hdl/"]'),
                        "submodule pointer": ("is_submodule_path(clean) or ", ""),
                        "empty delta": ("not changed or ", ""),
                    }[case.label]
                    assert pristine.count(old) == 1, f"mutation anchor drift: {case.label}"
                    try:
                        classifier.write_text(pristine.replace(old, new))
                        check(f"{workflow} {case.label} rule-removal mutation rejected",
                              execute(root, script, case.live, case.head, case.head,
                                      inputs={"ACT": "true"}) != expected)
                    finally:
                        classifier.write_text(pristine)
            case = cases[0]
            check(f"{workflow} missing hosted merge refuses",
                  refuses(root, script, case, "0" * 40, {}))
            check(f"{workflow} missing replay base refuses",
                  refuses(root, script, case, case.head,
                          {"ACT": "true", "PR_BASE_REF": "missing"}))
            git(root, "update-ref", "refs/remotes/origin/dev", case.live)
            check(f"{workflow} missing replay head refuses",
                  refuses(root, script, case, case.head,
                          {"ACT": "true", "PR_HEAD_SHA": "0" * 40}))
            git(root, "checkout", "--quiet", "--detach", ambiguous.head)
            git(root, "update-ref", "refs/remotes/origin/dev", ambiguous.live)
            check(f"{workflow} ambiguous replay base refuses",
                  refuses(root, script, ambiguous, ambiguous.head, {"ACT": "true"}))
            mutant = script.replace("git merge-base --all", "git merge-base")
            check(f"{workflow} arbitrary merge-base mutation rejected",
                  not refuses(root, mutant, ambiguous, ambiguous.head, {"ACT": "true"}))
            if workflow == "rtl-fast.yml":
                case = cases[0]
                check("fast push retains before-to-after comparison",
                      execute(root, script, case.live, case.recorded, case.recorded,
                              inputs={"EVENT_NAME": "push"})
                      == (["hdl/base.sv"], "true"))
    return int(failures)
