#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R276-6 reviewer probe: prove a commit range changes only comments under hdl/.

For every hdl/ path that differs between OLD and NEW, strip // line comments
and /* */ block comments (string literals are left alone; none of the files
use comment tokens inside strings), collapse whitespace, and compare the token
streams. Prints one line per file; exit 0 when every file is equal after
stripping. Usage: hdl_comment_only.py <repo> <old> <new>
"""
import re
import subprocess
import sys


def strip(src: str) -> list[str]:
    src = re.sub(r"/\*.*?\*/", " ", src, flags=re.S)
    src = re.sub(r"//[^\n]*", " ", src)
    return src.split()


def main() -> int:
    repo, old, new = sys.argv[1:4]
    names = subprocess.run(["git", "-C", repo, "diff", "--name-only", old, new, "--", "hdl/"],
                           capture_output=True, text=True, check=True).stdout.split()
    ok = True
    for n in names:
        a = subprocess.run(["git", "-C", repo, "show", f"{old}:{n}"], capture_output=True, text=True).stdout
        b = subprocess.run(["git", "-C", repo, "show", f"{new}:{n}"], capture_output=True, text=True).stdout
        same = strip(a) == strip(b)
        ok &= same
        print(f"{'COMMENT-ONLY' if same else 'CODE-CHANGED'} {n} ({len(strip(b))} code tokens)")
    print(f"files={len(names)} verdict={'comment-only' if ok else 'code changed'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
