#!/usr/bin/env python3
"""Prove the live-dev merge is disjoint and preserves the complete issue patch.

Usage: integration_proof.py BEFORE_HEAD DEV MERGE_RESULT_TREE_OR_COMMIT
Prints JSON: path sets, intersection, and SHA-256 of the issue patch before
(merge-base(BEFORE_HEAD, DEV)..BEFORE_HEAD) and after (DEV..MERGE) integration.
"""
import hashlib, json, subprocess, sys

def git(*a: str) -> bytes:
    return subprocess.run(["git", *a], check=True, capture_output=True).stdout

before, dev, after = sys.argv[1:4]
old_base = git("merge-base", before, dev).decode().strip()
issue = sorted(git("diff", "--name-only", old_base, before).decode().split())
devp = sorted(git("diff", "--name-only", old_base, dev).decode().split())
p_before = git("diff", "--binary", "--full-index", old_base, before)
p_after = git("diff", "--binary", "--full-index", dev, after)
dev_before = git("diff", "--binary", "--full-index", old_base, dev)
dev_after = git("diff", "--binary", "--full-index", before, after)
print(json.dumps({
    "before_head": git("rev-parse", before).decode().strip(),
    "dev": git("rev-parse", dev).decode().strip(),
    "after": git("rev-parse", after).decode().strip(),
    "old_merge_base": old_base,
    "issue_paths": issue, "dev_paths": devp,
    "intersection": sorted(set(issue) & set(devp)),
    "issue_patch_sha256_before": hashlib.sha256(p_before).hexdigest(),
    "issue_patch_sha256_after": hashlib.sha256(p_after).hexdigest(),
    "issue_patch_identical": p_before == p_after,
    "dev_patch_sha256_before": hashlib.sha256(dev_before).hexdigest(),
    "dev_patch_sha256_after": hashlib.sha256(dev_after).hexdigest(),
    "dev_patch_identical": dev_before == dev_after,
}, indent=2))
