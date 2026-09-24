#!/usr/bin/env python3
"""Compare comment-free RTL token streams between two commits of one Git repo.

Usage: rtl_comment_free_identity.py <repo> <base> <head>

Strips // and /* */ comments (string-literal aware), collapses whitespace,
then compares every tracked *.sv/*.svh/*.v/*.vh blob present at either commit.
Also runs two in-memory controls that must be detected as differences:
  1. aecp_ctlr_diag tie changed from 32'd0 to 32'd1 in milan_datapath.sv;
  2. the A_CTLR_DIAG read-mux arm retargeted in milan_csr.sv.
Exit 0 only if every file is identical and both controls are detected.
"""
import re
import subprocess
import sys

EXTS = (".sv", ".svh", ".v", ".vh")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True,
                          capture_output=True).stdout


def strip(src):
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
            i = n if j < 0 else j + 2
            out.append(" ")
        else:
            out.append(c)
            i += 1
    return " ".join("".join(out).split())


def files(repo, rev):
    names = git(repo, "ls-tree", "-r", "--name-only", rev).decode().split("\n")
    return {f for f in names if f.endswith(EXTS)}


def blob(repo, rev, path):
    return git(repo, "show", f"{rev}:{path}").decode("utf-8", "replace")


def main():
    repo, base, head = sys.argv[1:4]
    fb, fh = files(repo, base), files(repo, head)
    ok = True
    if fb != fh:
        print("FILESET-DIFF", sorted(fb ^ fh))
        ok = False
    same = differ = 0
    for p in sorted(fb & fh):
        if strip(blob(repo, base, p)) == strip(blob(repo, head, p)):
            same += 1
        else:
            differ += 1
            print("DIFF", p)
    print(f"rtl_files={len(fb & fh)} identical={same} differ={differ}")
    ok = ok and differ == 0

    dp = "hdl/milan/milan_datapath.sv"
    h = blob(repo, head, dp)
    tie = "assign aecp_ctlr_diag = 32'd0;"
    assert h.count(tie) == 1, "tie not found exactly once"
    m1 = strip(h.replace(tie, "assign aecp_ctlr_diag = 32'd1;")) != strip(blob(repo, base, dp))
    print("CONTROL1 nonzero tie detected:", m1)

    cs = "hdl/common/csr/milan_csr.sv"
    h = blob(repo, head, cs)
    arm = "A_CTLR_DIAG:  live_mux = i_ctlr_diag;"
    assert h.count(arm) == 1, "arm not found exactly once"
    m2 = strip(h.replace(arm, "A_CTLR_DIAG:  live_mux = i_i2spb_dbg;")) != strip(blob(repo, base, cs))
    print("CONTROL2 retargeted mux arm detected:", m2)

    ok = ok and m1 and m2
    print("RESULT", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
