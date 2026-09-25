#!/usr/bin/env python3
"""Check that the merge head's CHANGELOG.md is exactly the union of both parents'
Unreleased additions, verbatim, and nothing else. Usage: run inside the clone.
Args: MERGE OURS THEIRS BASE (commits)."""
import subprocess, sys

def show(rev):
    return subprocess.run(["git", "show", f"{rev}:CHANGELOG.md"], check=True,
                          capture_output=True, text=True).stdout.splitlines()

def section(lines, heading):
    i = lines.index(heading)
    j = i + 1
    while j < len(lines) and not lines[j].startswith("## "):
        j += 1
    return lines[i:j]

merge, ours, theirs, base = sys.argv[1:5]
M, O, T, B = show(merge), show(ours), show(theirs), show(base)
rh, ph = "## Unreleased - render setpoint state", "## Unreleased - processor pin 990f9652"
rl = [l for l in O if l.startswith("- **[Unreleased - render setpoint state]")]
pl = [l for l in T if l.startswith("- **[Unreleased - processor pin 990f9652]")]
ok = True
def chk(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name); ok &= cond
chk("render contents line unique in ours", len(rl) == 1)
chk("pin contents line unique in theirs", len(pl) == 1)
rs, ps = section(O, rh), section(T, ph)
ms_r, ms_p = section(M, rh), section(M, ph)
chk("render section verbatim in merge", ms_r == rs)
chk("pin section verbatim in merge", ms_p == ps)
chk("render contents line verbatim in merge", M.count(rl[0]) == 1)
chk("pin contents line verbatim in merge", M.count(pl[0]) == 1)
def drop(lines, sec, cline):
    out, i = [], 0
    s = lines.index(sec[0])
    out = lines[:s] + lines[s+len(sec):]
    out.remove(cline)
    return out
chk("merge minus render additions == theirs", drop(M, rs, rl[0]) == T)
chk("merge minus pin additions == ours", drop(M, ps, pl[0]) == O)
chk("render section absent from base", rh not in B)
chk("pin section absent from base", ph not in B)
print("RESULT", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
