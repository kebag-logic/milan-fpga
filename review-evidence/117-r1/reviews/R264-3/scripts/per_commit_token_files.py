#!/usr/bin/env python3
"""Per commit, list the files carrying one labelled token (raw, case-insensitive).

Usage: per_commit_token_files.py GITDIR TOKENS.tsv LABEL REV [REV...]
Prints commit, file count and paths; never the token.
"""
import ast, re, subprocess, sys

gitdir, tokfile, label = sys.argv[1:4]
tok = next(ast.literal_eval(l.rstrip("\n").split("\t", 3)[3]) for l in open(tokfile) if l.split("\t")[0] == label)
for rev in sys.argv[4:]:
    out = subprocess.run(["git", "--git-dir", gitdir, "grep", "-l", "-i", "-a", "-F", tok.decode(), rev],
                         capture_output=True).stdout.decode().split()
    print(f"COMMIT {rev} token={label} files={len(out)}")
    for p in out:
        print(f"    {p.split(':', 1)[1]}")
