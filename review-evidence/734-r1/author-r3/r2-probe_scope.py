#!/usr/bin/env python3
"""Reviewer probe for PR #735 scope steps.

Usage: probe_scope.py <repo-clone> <workdir>

Extracts the three PR scope step bodies with PyYAML (independently of the
candidate's own extractor) at two revisions -- the reviewed head and its
parent -- and executes them, with the classifier selftest call neutralised, on:

  B16   the real PR #725 history: recorded base 49da9fd9, head f1b2489f,
        hosted checkout = the merge commit that landed (6c810c45).
  REV   a synthetic lane that opens on a recorded base, merges a newer dev
        commit D that edits hdl/x.sv, then restores hdl/x.sv to the recorded
        base's content (a merge resolution or revert), plus a docs edit.
        Variant REV+E adds a later unrelated dev RTL commit E to the live base.
  XX    a criss-cross history (two merge bases) to record what `git diff A...B`
        does when the merge base is ambiguous.

Prints one JSON object per case. Exit 0 always; the oracle is the reader's.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

HEAD = "0519ff3684258482a56892056edbfbb65c186f88"
PARENT = "a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0"
STEPS = (("rtl.yml", "full-ci-gate", "gate"),
         ("rtl-fast.yml", "changes", "scope"),
         ("elaborate.yml", "elaborate", "scope"))
SELFTEST = "python3 scripts/ci_scope.py --selftest"


def git(root, *args, check=True):
    r = subprocess.run(["git", "-c", "core.hooksPath=/dev/null",
                        "-c", "user.name=Probe", "-c", "user.email=probe@example.invalid",
                        "-c", "advice.detachedHead=false",
                        "-C", str(root), *args], text=True, capture_output=True)
    if check and r.returncode:
        raise RuntimeError(f"git {args}: {r.stderr}")
    return r.stdout.strip() if check else r


def bodies(repo: Path, rev: str) -> dict[str, str]:
    out = {}
    for wf, job, sid in STEPS:
        doc = yaml.safe_load(git(repo, "show", f"{rev}:.github/workflows/{wf}"))
        step = next(s for s in doc["jobs"][job]["steps"] if s.get("id") == sid)
        body = step["run"]
        assert body.count(SELFTEST) == 1, (wf, rev)
        out[wf] = body.replace(SELFTEST, ":")
    return out


def run_body(root: Path, body: str, base: str, head: str, sha: str,
             event: str = "pull_request") -> dict:
    with tempfile.TemporaryDirectory(prefix="probe-") as raw:
        env = dict(os.environ, EVENT_NAME=event, PR_BASE_SHA=base, PR_HEAD_SHA=head,
                   GITHUB_SHA=sha, PR_DRAFT="false", PUSH_BEFORE_SHA=base,
                   GITHUB_OUTPUT=f"{raw}/out", RUNNER_TEMP=raw)
        r = subprocess.run(["bash", "-euo", "pipefail", "-c", body], cwd=root,
                           env=env, capture_output=True, text=True)
        changed = [p for p in Path(raw).glob("changed*")]
        files = changed[0].read_text().split() if changed else None
        outs = dict(l.split("=", 1) for l in Path(raw, "out").read_text().split()) \
            if Path(raw, "out").exists() else {}
        return {"rc": r.returncode, "n": None if files is None else len(files),
                "files": files if files is not None and len(files) <= 6 else "...",
                "rtl": outs.get("rtl"), "stderr": r.stderr.strip()[-300:]}


def classifier(root: Path, repo: Path) -> None:
    # Use the reviewed head's classifier in every fixture.
    (root / "scripts").mkdir(exist_ok=True)
    (root / "scripts/ci_scope.py").write_text(git(repo, "show", f"{HEAD}:scripts/ci_scope.py") + "\n")


def commit(root, parent, path, text, msg="c"):
    git(root, "checkout", "--quiet", "--detach", parent)
    p = root / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    git(root, "add", path)
    git(root, "commit", "--quiet", "-m", msg)
    return git(root, "rev-parse", "HEAD")


def case_b16(repo: Path, work: Path, new: dict, old: dict) -> None:
    wt = work / "b16"
    git(repo, "worktree", "add", "--quiet", "--detach", str(wt), "6c810c45ac4ac7d5b45797430753020c9ea31d86")
    try:
        (wt / "scripts/ci_scope.py").write_text(git(repo, "show", f"{HEAD}:scripts/ci_scope.py") + "\n")
        for label, bs in (("head", new), ("parent", old)):
            for wf, body in bs.items():
                res = run_body(wt, body, "49da9fd9", "f1b2489f",
                               git(wt, "rev-parse", "HEAD"))
                print(json.dumps({"case": "B16 hosted checkout = landed merge 6c810c45",
                                  "bodies": label, "workflow": wf, **res}))
        print(json.dumps({"case": "B16 counts",
                          "two_dot_no_renames": len(git(repo, "diff", "--no-renames", "--name-only", "49da9fd9", "f1b2489f").split()),
                          "two_dot_default": len(git(repo, "diff", "--name-only", "49da9fd9", "f1b2489f").split()),
                          "merge_base": git(repo, "diff", "--no-renames", "--name-only", "49da9fd9...f1b2489f").split()}))
    finally:
        git(repo, "worktree", "remove", "--force", str(wt))


def case_rev(repo: Path, work: Path, new: dict, old: dict) -> None:
    for with_e in (False, True):
        root = work / f"rev{int(with_e)}"
        root.mkdir()
        git(root, "init", "--quiet")
        classifier(root, repo)
        (root / "hdl").mkdir()
        (root / "hdl/x.sv").write_text("module x; // v0\nendmodule\n")
        (root / "docs").mkdir()
        (root / "docs/a.md").write_text("a\n")
        git(root, "add", ".")
        git(root, "commit", "--quiet", "-m", "fork")
        recorded = git(root, "rev-parse", "HEAD")           # PR opened here
        pr1 = commit(root, recorded, "docs/a.md", "a\nPR docs\n", "PR docs")
        d = commit(root, recorded, "hdl/x.sv", "module x; // v1 from dev\nendmodule\n", "dev D")
        live = d
        if with_e:
            live = commit(root, d, "hdl/y.sv", "module y; endmodule\n", "dev E")
        # Lane merges dev D, then restores hdl/x.sv to the recorded content.
        git(root, "checkout", "--quiet", "--detach", pr1)
        git(root, "merge", "--quiet", "--no-edit", d)
        (root / "hdl/x.sv").write_text("module x; // v0\nendmodule\n")
        git(root, "commit", "--quiet", "-am", "PR restores x.sv")
        head = git(root, "rev-parse", "HEAD")
        git(root, "checkout", "--quiet", "--detach", live)
        git(root, "merge", "--quiet", "--no-edit", head)
        merge = git(root, "rev-parse", "HEAD")
        comp = git(root, "diff", "--no-renames", "--name-only", live, merge).split()
        label = "REV+E" if with_e else "REV"
        print(json.dumps({"case": label, "composition_delta_vs_live_base": comp,
                          "merge_base(recorded,head)==recorded":
                              git(root, "merge-base", recorded, head) == recorded,
                          "live_base_three_dot": git(root, "diff", "--no-renames", "--name-only",
                                                     f"{live}...{head}").split()}))
        for bl, bs in (("head", new), ("parent", old)):
            for wf, body in bs.items():
                print(json.dumps({"case": label, "bodies": bl, "workflow": wf,
                                  **run_body(root, body, recorded, head, merge)}))


def case_xx(work: Path) -> None:
    root = work / "xx"
    root.mkdir()
    git(root, "init", "--quiet")
    (root / "f").write_text("0\n")
    git(root, "add", ".")
    git(root, "commit", "--quiet", "-m", "o")
    o = git(root, "rev-parse", "HEAD")
    a = commit(root, o, "a", "a\n")
    b = commit(root, o, "b", "b\n")
    git(root, "checkout", "--quiet", "--detach", a)
    git(root, "merge", "--quiet", "--no-edit", b)
    x = git(root, "rev-parse", "HEAD")
    git(root, "checkout", "--quiet", "--detach", b)
    git(root, "merge", "--quiet", "--no-edit", a)
    y = git(root, "rev-parse", "HEAD")
    r = git(root, "diff", "--name-only", f"{x}...{y}", check=False)
    print(json.dumps({"case": "XX criss-cross", "merge_bases": len(git(root, "merge-base", "--all", x, y).split()),
                      "rc": r.returncode, "stdout": r.stdout.strip(), "stderr": r.stderr.strip()}))


def main() -> int:
    repo, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    new, old = bodies(repo, HEAD), bodies(repo, PARENT)
    case_b16(repo, work, new, old)
    case_rev(repo, work, new, old)
    case_xx(work)
    return 0


if __name__ == "__main__":
    sys.exit(main())
