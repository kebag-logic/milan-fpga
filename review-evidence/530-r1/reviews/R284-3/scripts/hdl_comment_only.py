#!/usr/bin/env python3
"""Prove that every hdl/ change between two revisions is comment-only.

Usage: hdl_comment_only.py <repo> <old-rev> <new-rev> [<canary-old> <canary-new>]

For each .sv/.svh/.v file under hdl/ that differs between the revisions, the
blob at each side is stripped of // and /* */ comments (string-literal aware),
whitespace is normalised per token, and the results are compared. The file set
changed outside hdl/, the gitlinks and file modes are reported as well. An
optional canary pair must report DIFFERENT (proves the stripper can fail).
Exit 0 only if every hdl/ file is comment-identical and the canary differs.
"""
import hashlib
import re
import subprocess
import sys


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
            out.append(" ")
            i = n if j < 0 else j + 2
        else:
            out.append(c)
            i += 1
    toks = re.split(r"\s+", "".join(out))
    return " ".join(t for t in toks if t)


def changed(repo, a, b):
    raw = git(repo, "diff", "--raw", "--no-renames", a, b).decode()
    rows = []
    for line in raw.splitlines():
        meta, path = line.split("\t", 1)
        f = meta.split()
        rows.append((f[0][1:], f[1], f[4], path))
    return rows


def compare(repo, a, b, path):
    sa = strip(git(repo, "show", f"{a}:{path}").decode("utf-8", "replace"))
    sb = strip(git(repo, "show", f"{b}:{path}").decode("utf-8", "replace"))
    ha = hashlib.sha256(sa.encode()).hexdigest()
    hb = hashlib.sha256(sb.encode()).hexdigest()
    return ha == hb, ha, hb


def main():
    repo, a, b = sys.argv[1:4]
    ok = True
    rows = changed(repo, a, b)
    print(f"range {a}..{b}: {len(rows)} changed paths")
    for om, nm, st, path in rows:
        print(f"  {st} {om}->{nm} {path}")
        if om != nm:
            print("    MODE CHANGE"); ok = False
        if "160000" in (om, nm):
            print("    GITLINK CHANGE"); ok = False
    hdl = [r for r in rows if r[3].startswith("hdl/")]
    for om, nm, st, path in hdl:
        if st != "M" or not re.search(r"\.(sv|svh|v)$", path):
            print(f"  hdl non-modify or non-HDL: {path}"); ok = False
            continue
        same, ha, hb = compare(repo, a, b, path)
        print(f"  {path}: stripped {ha[:16]} vs {hb[:16]} -> "
              f"{'IDENTICAL' if same else 'DIFFERENT'}")
        ok &= same
    if len(sys.argv) == 6:
        ca, cb = sys.argv[4:6]
        crows = [r for r in changed(repo, ca, cb)
                 if r[3] == "hdl/milan/milan_datapath.sv"]
        if crows:
            same, ha, hb = compare(repo, ca, cb, crows[0][3])
            print(f"canary {ca}..{cb} milan_datapath.sv: "
                  f"{'IDENTICAL' if same else 'DIFFERENT'} (must be DIFFERENT)")
            ok &= not same
        else:
            print("canary: milan_datapath.sv unchanged in canary range"); ok = False
    print("RESULT", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
