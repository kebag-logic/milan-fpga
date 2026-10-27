#!/usr/bin/env python3
"""Verify the published evidence packet's MANIFEST.json against the bytes at a commit.

Usage: python3 -I verify_manifest.py <evidence git dir> <commit> <packet prefix> [subtree]

Every manifest entry whose file starts with [subtree] must exist at
<commit>:<packet prefix>/<file> with that published_sha256, and every blob
under the subtree must be listed. Prints one line per mismatch and a summary.
"""

import hashlib
import json
import subprocess
import sys


def git(repo: str, *args: str) -> bytes:
    return subprocess.run(["git", "-C", repo, *args], check=True,
                          capture_output=True).stdout


def main() -> int:
    repo, commit, prefix = sys.argv[1:4]
    sub = sys.argv[4] if len(sys.argv) > 4 else ""
    entries = json.loads(git(repo, "show", f"{commit}:{prefix}/MANIFEST.json"))
    listed = {e["file"]: e["published_sha256"] for e in entries
              if e["file"].startswith(sub)}
    tree = git(repo, "ls-tree", "-r", "--name-only", commit, f"{prefix}/{sub}")
    blobs = {p[len(prefix) + 1:] for p in tree.decode().splitlines()}
    bad = 0
    for name, want in sorted(listed.items()):
        got = hashlib.sha256(git(repo, "show", f"{commit}:{prefix}/{name}")).hexdigest()
        if got != want:
            print("MISMATCH", name, got, want)
            bad += 1
    for name in sorted(blobs - set(listed)):
        print("UNLISTED", name)
        bad += 1
    print(f"MANIFEST {sub or '*'}: {len(listed)} listed, {len(blobs)} blobs, "
          f"{bad} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
