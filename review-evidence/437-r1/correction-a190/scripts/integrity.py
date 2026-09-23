#!/usr/bin/env python3
"""The lane's identity at HEAD: head, tree, parents, base, cleanliness,
commit messages, changed paths and gitlinks. Usage: integrity.py OUT.json"""
import json, subprocess, sys
from pathlib import Path

LANE = "$LANES/437-container-paragraph-scopes"
DEV = "574c29fa111c74e5e5ed63e4670aff1f492e28e2"
START = "4741498f3b2b4f67f431037d327c96cf65691278"


def git(*a):
    return subprocess.run(["git", "-C", LANE, *a], capture_output=True, text=True, check=True).stdout


def main():
    head = git("rev-parse", "HEAD").strip()
    mb = git("merge-base", "origin/dev", "HEAD").strip()
    commits = []
    for sha in git("rev-list", f"{START}..HEAD").split():
        body = git("log", "-1", "--format=%B", sha).rstrip("\n")
        commits.append({"sha": sha, "parents": git("log", "-1", "--format=%P", sha).split(),
                        "message": body, "one_line": "\n" not in body,
                        "trailers": git("log", "-1", "--format=%(trailers)", sha).strip()})
    links = ("protocol-processor", "gptp-processor", "third_party/verilog-axis", "external", ".gitmodules")
    rec = {"head": head, "tree": git("rev-parse", "HEAD^{tree}").strip(),
           "branch": git("rev-parse", "--abbrev-ref", "HEAD").strip(),
           "origin_dev": git("rev-parse", "origin/dev").strip(), "merge_base": mb,
           "base_is_dev_tip": mb == git("rev-parse", "origin/dev").strip() == DEV,
           "clean": git("status", "--porcelain=v1", "--untracked-files=all") == "",
           "commits_since_start": commits,
           "paths_vs_merge_base": git("diff", "--name-status", mb, "HEAD").splitlines(),
           "gitlinks_equal_dev": git("ls-tree", DEV, "--", *links) == git("ls-tree", "HEAD", "--", *links),
           "gitlinks_equal_start": git("ls-tree", START, "--", *links) == git("ls-tree", "HEAD", "--", *links)}
    Path(sys.argv[1]).write_text(json.dumps(rec, indent=1) + "\n")
    print(json.dumps({k: v for k, v in rec.items() if k != "commits_since_start"}, indent=1))
    for c in commits:
        print(c["sha"], c["one_line"], repr(c["trailers"]), c["message"])
    return 0 if rec["clean"] and rec["base_is_dev_tip"] and all(c["one_line"] and not c["trailers"] for c in commits) else 1


if __name__ == "__main__":
    sys.exit(main())
