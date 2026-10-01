#!/usr/bin/env python3
"""Compare the lane's own delta (base..lane) with the merged delta (main..head),
file by file, as ordered lists of removed and added lines. Prints every line
that appears in one side only, after an optional rename map on the lane side.
Usage: compose_check.py REPO BASE LANE MAIN HEAD"""
import subprocess, sys, difflib

repo, base, lane, main, head = sys.argv[1:6]
RENAMES = [("F29 BIND_RX cdl 84", "F30 BIND_RX cdl 84"),
           ("F29 PROBE_TX cdl 84", "F30 PROBE_TX cdl 84"),
           ("F29 truncated reference", "F30 truncated reference"),
           ("// ---- F29: the 96-B IEEE", "// ---- F30: the 96-B IEEE"),
           ("PROBE_TX (F29, issue #45)", "PROBE_TX (F30, issue #45)"),
           ("| M5 | ACMP accepted only at cdl 44", "| M6 | ACMP accepted only at cdl 44"),
           ("F29: both 96-B forms", "F30: both 96-B forms")]

def git(*a):
    return subprocess.run(["git", "-C", repo, *a], check=True,
                          capture_output=True, text=True).stdout

def changed(a, b):
    return [l for l in git("diff", "--name-only", a, b).splitlines() if l]

def pm(a, b, path):
    out = git("diff", "-U0", a, b, "--", path)
    minus, plus = [], []
    for l in out.splitlines():
        if l.startswith("---") or l.startswith("+++"):
            continue
        if l.startswith("-"):
            minus.append(l[1:])
        elif l.startswith("+"):
            plus.append(l[1:])
    return minus, plus

def ren(lines):
    out = []
    for l in lines:
        for a, b in RENAMES:
            l = l.replace(a, b)
        out.append(l)
    return out

files = sorted(set(changed(base, lane)) | set(changed(main, head)))
total = 0
for f in files:
    lm, lp = pm(base, lane, f)
    hm, hp = pm(main, head, f)
    lm, lp = ren(lm), ren(lp)
    diffs = []
    for tag, x, y in (("removed", lm, hm), ("added", lp, hp)):
        for d in difflib.unified_diff(x, y, lineterm="", n=0):
            if d.startswith(("---", "+++", "@@")):
                continue
            diffs.append(f"  {tag}: {'lane-only' if d[0]=='-' else 'merged-only'}: {d[1:]}")
    print(f"{f}: lane -{len(lm)}/+{len(lp)}  merged -{len(hm)}/+{len(hp)}  "
          f"{'IDENTICAL after renames' if not diffs else str(len(diffs)) + ' line(s) differ'}")
    for d in diffs:
        print(d)
    total += len(diffs)
print(f"TOTAL differing lines: {total}")
