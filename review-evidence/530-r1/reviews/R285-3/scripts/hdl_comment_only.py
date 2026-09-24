#!/usr/bin/env python3
"""Prove that the hdl/ delta between two commits is comments only.

Usage: hdl_comment_only.py <repo> <base> <head> [<canary_base> <canary_head>]

1. Every changed (+/-) line of `git diff -U0 base head -- hdl/` must be a
   whole-line `//` comment and must not carry a tool metacomment token
   (verilator / synopsys / pragma / translate_ / lint_).
2. Every hdl/ file touched is compared after a string-aware strip of `//`
   and `/* */` comments and whitespace normalisation; the stripped bytes must
   be identical at base and head.
3. Optional canary: the same strip on a pair known to differ in logic must
   report DIFFERENT, proving the comparator can fail.
Exit 0 only if 1 and 2 hold (and 3 reports DIFFERENT when given).
"""
import hashlib
import re
import subprocess
import sys

META = re.compile(r"verilator|synopsys|pragma|translate_|lint_", re.I)


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True,
                          capture_output=True).stdout


def strip(src: str) -> str:
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c == '"':
            j = i + 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == "\\" else 1
            out.append(src[i:j + 1])
            i = j + 1
        elif src.startswith("//", i):
            j = src.find("\n", i)
            i = n if j < 0 else j
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2)
            if META.search(src[i:(n if j < 0 else j)]):
                out.append(src[i:(n if j < 0 else j + 2)])  # keep metacomments
            out.append(" ")
            i = n if j < 0 else j + 2
        else:
            out.append(c)
            i += 1
    return " ".join("".join(out).split())


def stripped(repo, rev, path):
    try:
        blob = git(repo, "show", f"{rev}:{path}").decode()
    except subprocess.CalledProcessError:
        return None
    return strip(blob)


def main():
    repo, base, head = sys.argv[1:4]
    ok = True
    diff = git(repo, "diff", "-U0", base, head, "--", "hdl/").decode()
    files = re.findall(r"^\+\+\+ b/(\S+)", diff, re.M)
    changed = [l for l in diff.splitlines()
               if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    bad = [l for l in changed if not l[1:].lstrip().startswith("//")]
    meta = [l for l in changed if META.search(l)]
    print(f"hdl files changed {base[:8]}..{head[:8]}: {files}")
    print(f"changed lines: {len(changed)}  non-comment: {len(bad)}  "
          f"metacomment-token: {len(meta)}")
    for l in bad + meta:
        print("  OFFENDING:", l)
    ok &= not bad and not meta
    for f in files:
        a, b = stripped(repo, base, f), stripped(repo, head, f)
        ha = hashlib.sha256((a or "").encode()).hexdigest()[:16]
        hb = hashlib.sha256((b or "").encode()).hexdigest()[:16]
        same = a is not None and a == b
        print(f"stripped {f}: base {ha} head {hb} -> "
              f"{'IDENTICAL' if same else 'DIFFERENT'}")
        ok &= same
    if len(sys.argv) == 7:
        cb, ch, cf = sys.argv[4], sys.argv[5], sys.argv[6]
        a, b = stripped(repo, cb, cf), stripped(repo, ch, cf)
        print(f"canary {cf} {cb[:8]} vs {ch[:8]}: "
              f"{'IDENTICAL' if a == b else 'DIFFERENT'}")
        ok &= a != b
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
