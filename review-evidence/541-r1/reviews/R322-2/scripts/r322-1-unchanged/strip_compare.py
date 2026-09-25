#!/usr/bin/env python3
"""Compare comment-stripped KL_crf_rx.sv between two commits.

Usage: strip_compare.py <repo> <base> <head> [path]
Strips // and /* */ comments outside string literals, drops blank lines and
trailing whitespace, then compares token streams and line streams.
Exit 0 when identical, 1 otherwise.
"""
import hashlib
import subprocess
import sys


def strip(text: str) -> str:
    out, i, n = [], 0, len(text)
    in_str = False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1]); i += 2; continue
            if c == '"':
                in_str = False
            i += 1
        elif c == '"':
            in_str = True; out.append(c); i += 1
        elif text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            if j < 0:
                raise SystemExit("unterminated block comment")
            out.append(" " if "\n" not in text[i:j] else "\n" * text[i:j].count("\n"))
            i = j + 2
        else:
            out.append(c); i += 1
    lines = [l.rstrip() for l in "".join(out).splitlines()]
    return "\n".join(l for l in lines if l.strip()) + "\n"


def main() -> int:
    repo, base, head = sys.argv[1:4]
    path = sys.argv[4] if len(sys.argv) > 4 else "hdl/ieee1722/crf/KL_crf_rx.sv"
    res = {}
    for rev in (base, head):
        blob = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                              check=True, capture_output=True, text=True).stdout
        s = strip(blob)
        res[rev] = s
        print(f"{rev} raw_sha256={hashlib.sha256(blob.encode()).hexdigest()} "
              f"stripped_sha256={hashlib.sha256(s.encode()).hexdigest()} "
              f"stripped_lines={s.count(chr(10))} tokens={len(s.split())}")
    same_lines = res[base] == res[head]
    same_tokens = res[base].split() == res[head].split()
    print(f"stripped_lines_identical={same_lines} stripped_tokens_identical={same_tokens}")
    return 0 if (same_lines and same_tokens) else 1


if __name__ == "__main__":
    raise SystemExit(main())
