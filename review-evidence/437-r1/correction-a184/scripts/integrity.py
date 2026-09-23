#!/usr/bin/env python3
"""Final integrity of the lane: exact head/tree/base, clean tree and index,
unchanged submodule gitlinks and .gitmodules, one-line trailer-free commit
messages for this author's commits, and the path scope against live dev.

Usage: integrity.py OUT.json
"""
import json
import subprocess
import sys
from pathlib import Path

LANE = "$LANES/437-container-paragraph-scopes"
DEV = "483a133ed08867ea0d300d2b4a027b5b48a4282f"
BASE = "88e9276b2a220c716f64a843f7e1eb8f9265e896"
START = "b5e6c23e1b9802b5cacbc62db212064d7e429862"


def git(*a: str) -> str:
    return subprocess.run(["git", "-C", LANE, *a], check=True, capture_output=True, text=True).stdout


def gitlinks(rev: str) -> dict[str, str]:
    out = {}
    for line in git("ls-tree", "-r", rev).splitlines():
        meta, path = line.split("\t", 1)
        mode, kind, oid = meta.split()
        if kind == "commit":
            out[path] = oid
    return out


def main() -> int:
    head = git("rev-parse", "HEAD").strip()
    status = git("status", "--porcelain=v1", "--untracked-files=all", "--ignore-submodules=none")
    unstaged = subprocess.run(["git", "-C", LANE, "diff", "--quiet"]).returncode
    staged = subprocess.run(["git", "-C", LANE, "diff", "--cached", "--quiet"]).returncode
    links = {r: gitlinks(r) for r in ("HEAD", DEV, BASE, START)}
    sub_status = git("submodule", "status").splitlines()
    mine = git("rev-list", "HEAD", f"^{START}", f"^{DEV}").split()
    messages = {c: git("log", "-1", "--format=%B", c).rstrip("\n") for c in mine}
    doc = {
        "head": head, "tree": git("rev-parse", "HEAD^{tree}").strip(),
        "parents": git("log", "-1", "--format=%P", "HEAD").split(),
        "live_dev": DEV, "merge_base_with_live_dev": git("merge-base", "HEAD", DEV).strip(),
        "descends_from_live_dev": subprocess.run(["git", "-C", LANE, "merge-base", "--is-ancestor", DEV,
                                                  "HEAD"]).returncode == 0,
        "branch": git("rev-parse", "--abbrev-ref", "HEAD").strip(),
        "status_porcelain": status, "worktree_clean": unstaged == 0 and status == "",
        "index_clean": staged == 0,
        "gitlinks": links["HEAD"],
        "gitlinks_equal_live_dev": links["HEAD"] == links[DEV],
        "gitlinks_equal_original_base": links["HEAD"] == links[BASE],
        "gitlinks_equal_starting_head": links["HEAD"] == links[START],
        "gitmodules_equal_live_dev": git("show", "HEAD:.gitmodules") == git("show", f"{DEV}:.gitmodules"),
        "submodule_status": sub_status,
        "submodules_at_gitlinks": all(not s.startswith(("+", "U")) for s in sub_status),
        "author_commits": mine,
        "author_messages": messages,
        "messages_one_line_no_trailers": all("\n" not in m and ":" not in m.split(" ", 1)[0]
                                             for m in messages.values()),
        "paths_changed_vs_live_dev": git("diff", "--name-status", DEV, "HEAD").splitlines(),
        "paths_changed_vs_starting_head": git("diff", "--name-status", START, "HEAD").splitlines(),
    }
    Path(sys.argv[1]).write_text(json.dumps(doc, indent=1) + "\n")
    ok = (doc["worktree_clean"] and doc["index_clean"] and doc["gitlinks_equal_live_dev"]
          and doc["gitlinks_equal_original_base"] and doc["gitmodules_equal_live_dev"]
          and doc["submodules_at_gitlinks"] and doc["messages_one_line_no_trailers"]
          and doc["descends_from_live_dev"])
    print(json.dumps({k: v for k, v in doc.items() if k not in ("author_messages",)}, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
