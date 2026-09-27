#!/usr/bin/env python3
"""Prove that SystemVerilog edits between two commits touch comments only.

Usage: sv_comment_only.py <repo> <old-rev> <new-rev> <path>...

For each path, both blobs are read with `git show`, every // and /* */
comment is removed (string literals are respected), whitespace runs are
collapsed, and the resulting token streams are compared. Exit 0 only when
every path is token-identical and at least one path's raw bytes differ.
"""
import re
import subprocess
import sys


def strip(text: str) -> str:
    out, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            out.append(text[i:j + 1])
            i = j + 1
        elif text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            if j < 0:
                raise SystemExit("unterminated block comment")
            out.append(" ")
            i = j + 2
        else:
            out.append(c)
            i += 1
    return " ".join(re.split(r"\s+", "".join(out))).strip()


def blob(repo: str, rev: str, path: str) -> str:
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                          check=True, capture_output=True,
                          text=True).stdout


def main() -> int:
    repo, old, new, *paths = sys.argv[1:]
    ok, any_raw = True, False
    for path in paths:
        a, b = blob(repo, old, path), blob(repo, new, path)
        raw_same = a == b
        any_raw |= not raw_same
        tok_same = strip(a) == strip(b)
        print(f"{path}: raw_identical={raw_same} "
              f"code_tokens_identical={tok_same} "
              f"code_chars={len(strip(b))}")
        ok &= tok_same
    print("RESULT", "COMMENT-ONLY" if ok and any_raw else "CODE-CHANGED"
          if not ok else "NO-CHANGE")
    return 0 if ok and any_raw else 1


if __name__ == "__main__":
    sys.exit(main())
