#!/usr/bin/env python3
"""Apply the repository's own privacy scrub rules to every blob of a git range.

Usage: repo_scrub_over_archive.py <repo-checkout-with-scripts/docs_check.py> <bare-repo> <label>=<A..B> ...

Imports SCRUB_RULES (IDENTITY_RULES + LOCAL_RULES) from the checkout's
scripts/docs_check.py unchanged and applies them line by line to every blob
reachable in each range, binary blobs included (decoded as latin-1, which the
repository gate itself skips), plus every commit message. Prints rule label,
object and line only; never the matched text.
"""
import importlib.util
import subprocess
import sys


def git(repo, *args, inp=None):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, input=inp).stdout


def main():
    checkout, repo, *scopes = sys.argv[1:]
    spec = importlib.util.spec_from_file_location("docs_check", f"{checkout}/scripts/docs_check.py")
    dc = importlib.util.module_from_spec(spec)
    sys.argv = [sys.argv[0]]
    spec.loader.exec_module(dc)
    rules = dc.SCRUB_RULES
    print(f"rules loaded: {len(rules)} ({', '.join(r[1] for r in rules)})")
    total = 0
    for sc in scopes:
        label, rng = sc.split("=", 1)
        a, b = rng.split("..", 1)
        objs = {}
        for line in git(repo, "rev-list", "--objects", b, "^" + a).decode().splitlines():
            p = line.split(" ", 1)
            if len(p) == 2:
                objs.setdefault(p[0], p[1])
        kinds = dict(l.split()[:2] for l in git(repo, "cat-file", "--batch-check", inp="\n".join(objs).encode()).decode().splitlines())
        items = [(f"commit:{c[:8]}", git(repo, "cat-file", "commit", c)) for c in git(repo, "rev-list", b, "^" + a).decode().split()]
        items += [(f"{o[:8]}:{p}", git(repo, "cat-file", "blob", o)) for o, p in objs.items() if kinds.get(o) == "blob"]
        hits = 0
        for name, data in items:
            text = data.decode("latin-1")
            for ln, line in enumerate(text.splitlines(), 1):
                for pat, lab, _ in rules:
                    if pat.search(line):
                        hits += 1
                        print(f"  HIT {label} {name}:{ln} rule='{lab}'")
        print(f"scope {label} ({rng}): {len(items)} objects scanned, hits {hits}")
        total += hits
    print(f"TOTAL hits: {total}")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
