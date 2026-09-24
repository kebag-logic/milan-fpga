#!/usr/bin/env python3
"""Compare SystemVerilog sources across git revisions with comments removed.

Usage: sv_strip_compare.py <repo> <path> <rev> [<rev> ...]

For each revision, reads <path> from the git object store (not the worktree),
removes // and /* */ comments outside string literals, collapses every run of
whitespace to one space, and prints the sha256 of the result. Exit 0 when all
revisions produce the same digest, 1 otherwise.
"""
import hashlib
import subprocess
import sys


def strip_comments(text: str) -> str:
    out = []
    i, n = 0, len(text)
    in_str = False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            out.append(c)
            i += 1
            continue
        if text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
            continue
        if text.startswith("/*", i):
            j = text.find("*/", i + 2)
            i = n if j < 0 else j + 2
            out.append(" ")
            continue
        out.append(c)
        i += 1
    return " ".join("".join(out).split())


def main() -> int:
    repo, path, revs = sys.argv[1], sys.argv[2], sys.argv[3:]
    digests = {}
    for rev in revs:
        blob = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                              check=True, capture_output=True).stdout
        digests[rev] = hashlib.sha256(
            strip_comments(blob.decode("utf-8")).encode()).hexdigest()
        print(f"{rev} {path} stripped-sha256 {digests[rev]}")
    same = len(set(digests.values())) == 1
    print("IDENTICAL" if same else "DIFFERENT")
    return 0 if same else 1


if __name__ == "__main__":
    sys.exit(main())
