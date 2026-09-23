#!/usr/bin/env python3
"""Prove a workflow change between two commits is comment-only.

usage: yaml_comment_only.py <repo> <old-rev> <new-rev> <path>

Three independent answers, all must agree:
  1. yaml.safe_load of both versions is equal (the data every reader parses);
  2. the sequences of non-comment lines are byte-identical;
  3. every line the diff adds or removes is a YAML comment line, and after the
     change each added comment line is not inside any run block scalar (the
     parsed step scripts are compared in 1, so a comment swallowed into a
     `run: |` body would already fail there; this names it).
Exit 0 only when all three hold.
"""
import difflib
import subprocess
import sys

import yaml


def show(repo: str, rev: str, path: str) -> str:
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], check=True,
                          capture_output=True, text=True).stdout


def main() -> int:
    repo, old_rev, new_rev, path = sys.argv[1:5]
    old, new = show(repo, old_rev, path), show(repo, new_rev, path)
    ok = True
    same = yaml.safe_load(old) == yaml.safe_load(new)
    print(f"1 parsed-yaml-equal={same}")
    ok &= same
    strip = lambda text: [l for l in text.splitlines() if not l.lstrip().startswith("#")]
    same_code = strip(old) == strip(new)
    print(f"2 non-comment-lines-identical={same_code} (old={len(strip(old))} new={len(strip(new))})")
    ok &= same_code
    changed = [l for l in difflib.unified_diff(old.splitlines(), new.splitlines(), lineterm="", n=0)
               if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    non_comment = [l for l in changed if not l[1:].lstrip().startswith("#")]
    print(f"3 changed-lines={len(changed)} non-comment-changed-lines={len(non_comment)}")
    for line in changed:
        print(f"   {line}")
    ok &= not non_comment and bool(changed)
    # Scripts as parsed: an added comment text must not appear inside any run body.
    added = [l[1:].strip() for l in changed if l.startswith("+")]
    runs = []
    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "run" and isinstance(v, str):
                    runs.append(v)
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    walk(yaml.safe_load(new))
    leaked = [a for a in added if any(a in r for r in runs)]
    print(f"   run-bodies={len(runs)} added-comment-lines-found-in-run-bodies={len(leaked)}")
    ok &= not leaked
    print("COMMENT-ONLY" if ok else "NOT COMMENT-ONLY")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
